//
//  FilterBank.swift
//  Camera
//
//  Created by Mihnea Rusu on 06/12/16.
//  Copyright © 2016 Matteo Caldari. All rights reserved.
//

import Foundation
import CoreImage

protocol OCRImageFilter {
    associatedtype ImageType
    func makeSepia() -> ImageType
}

extension CIImage : OCRImageFilter {
    typealias ImageType = CIImage
    
    /* Provides a number of filters for image processing. */
    
    /**
        Filters the image with a sepia filter at 50% intensity.
        
        - Returns: The modified image if the filter is available, or the original if not.
    */
    func makeSepia() -> ImageType {
        let filter = CIFilter(name: "CISepiaTone")
        filter?.setValue(self, forKey: kCIInputImageKey)
        filter?.setValue(0.5, forKey: kCIInputIntensityKey)
        if let outputImage = filter?.outputImage {
            return outputImage
        }
        
        return self
    }
    
    /**
        Filters the image brightness and contrast and turns it to black and white.
     
        - Parameters:
            - brightness: Brightness increase/decrease value [-1...1]
            - contrast: Contrast enhancement value (no upper bound)
     
        - Returns: The modified image if the filter is available, or the original if not.
    */
    func filterBW(brightness: NSNumber, contrast: NSNumber) -> ImageType {
        let filter = CIFilter(name: "CIColorControls")
        filter?.setValue(self, forKey: kCIInputImageKey)
        filter?.setValue(0.0, forKey: kCIInputSaturationKey)
        filter?.setValue(brightness, forKey: kCIInputBrightnessKey)
        filter?.setValue(contrast, forKey: kCIInputContrastKey)
        if let outputImage = filter?.outputImage {
            return outputImage
        }
        
        return self
    }
    
    /**
        Filters the image using a thresholding kernel.
     
        - Parameters:
            - min: Any intensity value below this will become black.
            - max: Any intensity value above this will become white.
     
        - Returns: The modified image if the filter is available, or the original if not.
    */
    func thresholded(min: NSNumber, max: NSNumber) -> ImageType {
        let thresholdKernel = CIColorKernel(string:
            "kernel vec4 thresholdKernel (" +
                "sampler src, " +
                "float min, " +
                "float max " +
                ")" +
            "{" +
                "vec4 pixValue;" +
                "vec3 blackThresholded, whiteThresholded;" +
                "pixValue = sample(src, samplerCoord(src));" +
                "blackThresholded = compare(pixValue.rgb - vec3(min, min, min), vec3(0.0, 0.0, 0.0), pixValue.rgb);" +
                "whiteThresholded = compare(vec3(max, max, max) - blackThresholded, vec3(1.0, 1.0, 1.0), blackThresholded);" +
                "return vec4(whiteThresholded.r, whiteThresholded.g, whiteThresholded.b, 1.0);" +
            "}"
        )
        
        if thresholdKernel != nil {
            let extent = self.extent
            let arguments = [self, min, max]
            
            return thresholdKernel!.apply(withExtent: extent, arguments: arguments)!
        }
        
        return self
    }
}
