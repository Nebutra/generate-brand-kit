#!/usr/bin/env swift

import AppKit
import Foundation
import Vision

struct Options {
    let input: URL
    let outputDirectory: URL
    let labels: [String]
    let canvasSize: Int
    let fillRatio: CGFloat
    let contrast: Float
    let pivot: Float
}

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data("error: \(message)\n".utf8))
    exit(1)
}

func parseOptions() -> Options {
    guard CommandLine.arguments.count >= 5 else {
        fail("usage: extract_wordmark_glyphs.swift input.png output-dir --labels A,B,C [--canvas 1024] [--fill-ratio 0.72]")
    }
    let input = URL(fileURLWithPath: CommandLine.arguments[1])
    let output = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)
    var values: [String: String] = [:]
    var index = 3
    while index < CommandLine.arguments.count {
        let key = CommandLine.arguments[index]
        guard key.hasPrefix("--"), index + 1 < CommandLine.arguments.count else {
            fail("expected --key value arguments")
        }
        values[key] = CommandLine.arguments[index + 1]
        index += 2
    }
    guard let rawLabels = values["--labels"] else { fail("--labels is required") }
    let labels = rawLabels.split(separator: ",").map(String.init)
    guard !labels.isEmpty else { fail("--labels must not be empty") }
    for label in labels {
        guard label.range(of: #"^[A-Za-z0-9][A-Za-z0-9._-]*$"#, options: .regularExpression) != nil else {
            fail("unsafe label: \(label)")
        }
    }
    let canvas = Int(values["--canvas"] ?? "1024") ?? 1024
    let fillRatio = CGFloat(Double(values["--fill-ratio"] ?? "0.72") ?? 0.72)
    guard canvas >= 128, fillRatio > 0.2, fillRatio < 0.95 else {
        fail("invalid canvas or fill ratio")
    }
    return Options(
        input: input,
        outputDirectory: output,
        labels: labels,
        canvasSize: canvas,
        fillRatio: fillRatio,
        contrast: Float(values["--contrast"] ?? "2.4") ?? 2.4,
        pivot: Float(values["--pivot"] ?? "0.72") ?? 0.72
    )
}

func appendContour(_ contour: VNContour, to path: CGMutablePath) throws {
    let polygon = try contour.polygonApproximation(epsilon: 0.00025)
    guard polygon.pointCount > 2 else { return }
    let points = polygon.normalizedPoints
    path.move(to: CGPoint(x: CGFloat(points[0].x), y: CGFloat(points[0].y)))
    for index in 1..<polygon.pointCount {
        path.addLine(to: CGPoint(x: CGFloat(points[index].x), y: CGFloat(points[index].y)))
    }
    path.closeSubpath()
    for child in contour.childContours {
        try appendContour(child, to: path)
    }
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
guard let observation = request.results?.first else { fail("no contour observation") }
let contours = observation.topLevelContours.sorted {
    $0.normalizedPath.boundingBox.minX < $1.normalizedPath.boundingBox.minX
}
guard contours.count == options.labels.count else {
    fail("expected \(options.labels.count) top-level glyphs, found \(contours.count); clean the source or adjust contour settings")
}

try? FileManager.default.createDirectory(at: options.outputDirectory, withIntermediateDirectories: true)
let canvasSize = options.canvasSize

for (label, contour) in zip(options.labels, contours) {
    guard let bitmap = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: canvasSize,
        pixelsHigh: canvasSize,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: 0,
        bitsPerPixel: 0
    ), let context = NSGraphicsContext(bitmapImageRep: bitmap) else {
        fail("cannot create \(label) canvas")
    }

    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = context
    NSColor.white.setFill()
    NSRect(x: 0, y: 0, width: canvasSize, height: canvasSize).fill()

    let bounds = contour.normalizedPath.boundingBox
    let maxDimension = CGFloat(canvasSize) * options.fillRatio
    let scale = min(maxDimension / bounds.width, maxDimension / bounds.height)
    let width = bounds.width * scale
    let height = bounds.height * scale
    let offsetX = (CGFloat(canvasSize) - width) / 2
    let offsetY = (CGFloat(canvasSize) - height) / 2

    let normalizedPath = CGMutablePath()
    do {
        try appendContour(contour, to: normalizedPath)
    } catch {
        fail("cannot simplify \(label): \(error)")
    }
    var transform = CGAffineTransform(
        a: scale,
        b: 0,
        c: 0,
        d: scale,
        tx: offsetX - bounds.minX * scale,
        ty: offsetY - bounds.minY * scale
    )
    guard let targetPath = normalizedPath.copy(using: &transform) else {
        fail("cannot transform \(label)")
    }
    context.cgContext.setFillColor(NSColor.black.cgColor)
    context.cgContext.addPath(targetPath)
    context.cgContext.drawPath(using: .eoFill)
    context.flushGraphics()
    NSGraphicsContext.restoreGraphicsState()

    guard let png = bitmap.representation(using: .png, properties: [:]) else {
        fail("cannot encode \(label)")
    }
    let target = options.outputDirectory.appendingPathComponent("\(label).png")
    do {
        try png.write(to: target)
    } catch {
        fail("cannot write \(target.path): \(error)")
    }
    print("\(label): \(target.path)")
}
