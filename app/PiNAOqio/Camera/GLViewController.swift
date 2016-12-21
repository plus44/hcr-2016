//
//  GLViewController.swift
//  Camera
//
//  Created by Matteo Caldari on 28/01/15.
//  Copyright (c) 2015 Matteo Caldari. All rights reserved.
//

import UIKit
import GLKit
import CoreImage
import OpenGLES

class GLViewController: UIViewController {


	var cameraController:CameraController!
	
	fileprivate var glContext:EAGLContext?
	fileprivate var ciContext:CIContext?
	fileprivate var renderBuffer:GLuint = GLuint()
	
	fileprivate var glView:GLKView {
		get {
			return view as! GLKView
		}
	}


	override func viewDidLoad() {
        super.viewDidLoad()
	
		glContext = EAGLContext(api: .openGLES2)
		
		
		glView.context = glContext!
//		glView.drawableDepthFormat = .Format24
		glView.transform = CGAffineTransform(rotationAngle: CGFloat(M_PI_2))
		if let window = glView.window {
			glView.frame = window.bounds
		}
		
		ciContext = CIContext(eaglContext: glContext!)

		cameraController = CameraController(previewType: .manual, delegate: self)
	}

	
	override func viewDidAppear(_ animated: Bool) {
		cameraController.startRunning()
	}
	
	
}

// MARK: CameraControllerDelegate
extension GLViewController : CameraControllerDelegate {
    
	func cameraController(_ cameraController: CameraController, didDetectFaces faces: [(id: Int, frame: CGRect)]) {
		
	}

	
	func cameraController(_ cameraController: CameraController, didOutputImage image: CIImage) {

		if glContext != EAGLContext.current() {
			EAGLContext.setCurrent(glContext)
		}
		
		glView.bindDrawable()

		ciContext?.draw(image, in:image.extent, from: image.extent)

		glView.display()
	}
}
