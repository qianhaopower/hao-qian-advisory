// cover_eyes.swift — are the eyes open in this picture? (COVER EYES LAW, Hao 2026-11-18: 「别让我光闭眼，封面别让我踩那些闭眼的」)
// Apple Vision face landmarks → eye aspect ratio (box height / box width of each eye's landmark points).
//   xcrun swiftc -O -o "$HOME/Video Studio/work/bin/cover_eyes" cover_eyes.swift -framework Vision -framework AppKit
//   cover_eyes a.png b.png …   →   path \t leftEAR \t rightEAR \t faceWidth(normalised)      (noface / noimage when it cannot tell)
// Driven by cover_eyes.py (frame extraction, thresholds, the pick); nothing else calls it directly.
import Foundation
import Vision
import AppKit

func ear(_ region: VNFaceLandmarkRegion2D?, _ w: CGFloat, _ h: CGFloat) -> Double {
    guard let r = region, r.pointCount >= 4 else { return -1 }
    let pts = r.pointsInImage(imageSize: CGSize(width: w, height: h))
    let xs = pts.map { $0.x }, ys = pts.map { $0.y }
    let bw = xs.max()! - xs.min()!, bh = ys.max()! - ys.min()!
    return bw > 0 ? Double(bh / bw) : -1
}

for path in CommandLine.arguments.dropFirst() {
    guard let img = NSImage(contentsOfFile: path),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { print("\(path)\tnoimage"); continue }
    let req = VNDetectFaceLandmarksRequest()
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    do { try handler.perform([req]) } catch { print("\(path)\tnoface"); continue }
    guard let obs = req.results?.max(by: { $0.boundingBox.width < $1.boundingBox.width }) else { print("\(path)\tnoface"); continue }
    let w = CGFloat(cg.width), h = CGFloat(cg.height)
    let l = ear(obs.landmarks?.leftEye, w, h), r = ear(obs.landmarks?.rightEye, w, h)
    print(String(format: "%@\t%.3f\t%.3f\t%.3f", path, l, r, Double(obs.boundingBox.width)))
}
