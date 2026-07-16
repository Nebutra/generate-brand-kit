#!/usr/bin/env swift

import AppKit
import Foundation
import Vision

struct Options {
    let input: URL
    let output: URL
    let title: String
    let epsilon: Float
    let minimumArea: Double
    let padding: Double
    let contrast: Float
    let pivot: Float
}

struct Polygon {
    let points: [CGPoint]
}

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data("error: \(message)\n".utf8))
    exit(1)
}

func parseOptions() -> Options {
    var values: [String: String] = [:]
    var index = 1
    while index < CommandLine.arguments.count {
        let key = CommandLine.arguments[index]
        guard key.hasPrefix("--"), index + 1 < CommandLine.arguments.count else {
            fail("expected --key value arguments")
        }
        values[key] = CommandLine.arguments[index + 1]
        index += 2
    }
    guard let input = values["--input"], let output = values["--output"] else {
        fail("usage: vectorize_glyph.swift --input glyph.png --output glyph.svg [--title name]")
    }
    return Options(
        input: URL(fileURLWithPath: input),
        output: URL(fileURLWithPath: output),
        title: values["--title"] ?? "Glyph",
        epsilon: Float(values["--epsilon"] ?? "0.0012") ?? 0.0012,
        minimumArea: Double(values["--min-area"] ?? "0.00008") ?? 0.00008,
        padding: Double(values["--padding"] ?? "0.015") ?? 0.015,
        contrast: Float(values["--contrast"] ?? "2.0") ?? 2.0,
        pivot: Float(values["--pivot"] ?? "0.72") ?? 0.72
    )
}

func polygonArea(_ points: [CGPoint]) -> Double {
    guard points.count > 2 else { return 0 }
    var sum = 0.0
    for index in points.indices {
        let next = points[(index + 1) % points.count]
        sum += Double(points[index].x * next.y - next.x * points[index].y)
    }
    return abs(sum) / 2.0
}

func collectPolygons(
    from contour: VNContour,
    epsilon: Float,
    minimumArea: Double,
    output: inout [Polygon]
) throws {
    let simplified = try contour.polygonApproximation(epsilon: epsilon)
    let pointer = simplified.normalizedPoints
    let points = (0..<simplified.pointCount).map { index in
        CGPoint(x: CGFloat(pointer[index].x), y: CGFloat(pointer[index].y))
    }
    if polygonArea(points) >= minimumArea {
        output.append(Polygon(points: points))
        for child in contour.childContours {
            try collectPolygons(
                from: child,
                epsilon: epsilon,
                minimumArea: minimumArea,
                output: &output
            )
        }
    }
}

func format(_ value: CGFloat) -> String {
    var text = String(format: "%.3f", Double(value))
    while text.contains(".") && text.hasSuffix("0") { text.removeLast() }
    if text.hasSuffix(".") { text.removeLast() }
    return text
}

func xmlEscape(_ value: String) -> String {
    value
        .replacingOccurrences(of: "&", with: "&amp;")
        .replacingOccurrences(of: "<", with: "&lt;")
        .replacingOccurrences(of: ">", with: "&gt;")
        .replacingOccurrences(of: "\"", with: "&quot;")
}

let options = parseOptions()
guard let image = NSImage(contentsOf: options.input) else {
    fail("cannot read \(options.input.path)")
}
var proposedRect = CGRect(origin: .zero, size: image.size)
guard let cgImage = image.cgImage(forProposedRect: &proposedRect, context: nil, hints: nil) else {
    fail("cannot decode \(options.input.path)")
}

let request = VNDetectContoursRequest()
request.contrastAdjustment = options.contrast
request.contrastPivot = NSNumber(value: options.pivot)
request.detectsDarkOnLight = true
request.maximumImageDimension = max(cgImage.width, cgImage.height)
do {
    try VNImageRequestHandler(cgImage: cgImage, orientation: .up).perform([request])
} catch {
    fail("Vision contour request failed: \(error)")
}
guard let observation = request.results?.first else {
    fail("Vision returned no contour observation")
}

var polygons: [Polygon] = []
do {
    for contour in observation.topLevelContours {
        try collectPolygons(
            from: contour,
            epsilon: options.epsilon,
            minimumArea: options.minimumArea,
            output: &polygons
        )
    }
} catch {
    fail("contour simplification failed: \(error)")
}
guard !polygons.isEmpty else { fail("no contours survived filtering") }

let imageWidth = CGFloat(cgImage.width)
let imageHeight = CGFloat(cgImage.height)
let transformed = polygons.map { polygon in
    polygon.points.map { point in
        CGPoint(x: point.x * imageWidth, y: (1 - point.y) * imageHeight)
    }
}
let allPoints = transformed.flatMap { $0 }
guard let first = allPoints.first else { fail("no contour points") }
var minimumX = first.x
var maximumX = first.x
var minimumY = first.y
var maximumY = first.y
for point in allPoints.dropFirst() {
    minimumX = min(minimumX, point.x)
    maximumX = max(maximumX, point.x)
    minimumY = min(minimumY, point.y)
    maximumY = max(maximumY, point.y)
}
let contentWidth = maximumX - minimumX
let contentHeight = maximumY - minimumY
let inset = max(contentWidth, contentHeight) * CGFloat(options.padding)
let viewBox = CGRect(
    x: minimumX - inset,
    y: minimumY - inset,
    width: contentWidth + inset * 2,
    height: contentHeight + inset * 2
)

let pathData = transformed.map { points -> String in
    guard let start = points.first else { return "" }
    let lines = points.dropFirst().map { "L \(format($0.x)) \(format($0.y))" }
    return (["M \(format(start.x)) \(format(start.y))"] + lines + ["Z"]).joined(separator: " ")
}.joined(separator: " ")

let svg = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="\(format(viewBox.minX)) \(format(viewBox.minY)) \(format(viewBox.width)) \(format(viewBox.height))" role="img" aria-labelledby="title">
  <title id="title">\(xmlEscape(options.title))</title>
  <path fill="currentColor" fill-rule="evenodd" d="\(pathData)"/>
</svg>
"""

do {
    try FileManager.default.createDirectory(
        at: options.output.deletingLastPathComponent(),
        withIntermediateDirectories: true
    )
    try svg.write(to: options.output, atomically: true, encoding: .utf8)
} catch {
    fail("cannot write \(options.output.path): \(error)")
}

let pointCount = polygons.reduce(0) { $0 + $1.points.count }
print("\(options.output.path): \(polygons.count) contours, \(pointCount) points")
