#!/usr/bin/env swift

import AppKit
import CoreText
import Foundation

func fail(_ message: String) -> Never {
    FileHandle.standardError.write(Data((message + "\n").utf8))
    exit(1)
}

guard CommandLine.arguments.count == 5 else {
    fail("usage: render_font_specimens.swift FONT.ttf FAMILY_NAME SOURCE_WORD OUTPUT_DIR")
}

let fontPath = CommandLine.arguments[1]
let familyName = CommandLine.arguments[2]
let sourceWord = CommandLine.arguments[3]
let outputDirectory = URL(fileURLWithPath: CommandLine.arguments[4], isDirectory: true)
try FileManager.default.createDirectory(at: outputDirectory, withIntermediateDirectories: true)

var registrationError: Unmanaged<CFError>?
guard CTFontManagerRegisterFontsForURL(URL(fileURLWithPath: fontPath) as CFURL, .process, &registrationError) else {
    fail("failed to register font: \(registrationError?.takeRetainedValue().localizedDescription ?? "unknown error")")
}

func render(_ text: String, name: String) throws {
    let width = 2400
    let height = 520
    guard let bitmap = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: width,
        pixelsHigh: height,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: 0,
        bitsPerPixel: 0
    ) else { fail("failed to allocate bitmap") }
    NSGraphicsContext.saveGraphicsState()
    guard let context = NSGraphicsContext(bitmapImageRep: bitmap) else { fail("failed to create graphics context") }
    NSGraphicsContext.current = context
    NSColor.white.setFill()
    NSRect(x: 0, y: 0, width: width, height: height).fill()
    let paragraph = NSMutableParagraphStyle()
    paragraph.alignment = .center
    guard let font = NSFont(
        name: familyName,
        size: name == "source-word" ? 250 : 138
    ) else {
        fail("registered family not found: \(familyName)")
    }
    let attributes: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor.black,
        .paragraphStyle: paragraph,
    ]
    let rect = NSRect(x: 80, y: 90, width: width - 160, height: height - 180)
    text.draw(in: rect, withAttributes: attributes)
    context.flushGraphics()
    NSGraphicsContext.restoreGraphicsState()
    guard let data = bitmap.representation(using: .png, properties: [:]) else { fail("failed to encode PNG") }
    try data.write(to: outputDirectory.appendingPathComponent("\(name).png"))
}

try render("ABCDEFGHIJKLMNOPQRSTUVWXYZ", name: "uppercase")
try render("abcdefghijklmnopqrstuvwxyz", name: "lowercase")
try render(sourceWord, name: "source-word")
print(outputDirectory.path)
