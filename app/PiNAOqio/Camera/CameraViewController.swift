//
//  CameraViewController.swift
//  Camera
//
//  Created by Matteo Caldari on 08/01/15.
//  Copyright (c) 2015 Matteo Caldari. All rights reserved.
//

import UIKit
import GLKit
import CoreImage
import OpenGLES

class CameraViewController : UIViewController, CameraSettingValueObserver {

	var cameraController:CameraController!
    var serverController : ServerController!
    var shouldContinueLongPolling : Bool = true

	@IBOutlet var videoPreviewView:GLKView!
	@IBOutlet var controlsView:UIView!
	@IBOutlet var facesView:UIView!
	
	@IBOutlet var focusButton:UIButton!
	@IBOutlet var exposureButton:UIButton!
	@IBOutlet var whiteBalanceButton:UIButton!
	@IBOutlet var optionsButton:UIButton!

	@IBOutlet var adjustingFocusIndicator:UIView!
	@IBOutlet var adjustingExposureIndicator:UIView!
	@IBOutlet var adjustingWhiteBalanceIndicator:UIView!
	
	@IBOutlet var currentValuesLabel:UILabel!
	
	fileprivate var currentControlsViewController:UIViewController?
	fileprivate var faceViews = [UIView]()
    
    fileprivate var glContext:EAGLContext?
    fileprivate var ciContext:CIContext?
    fileprivate var renderBuffer:GLuint = GLuint()
    
    fileprivate var glView:GLKView! {
        get {
            return videoPreviewView
        }
    }
    
    fileprivate var shouldCaptureCurrentCIImage : Bool = false
    fileprivate var currentCIImage : CIImage! = nil
    
    override func loadView() {
        super.loadView()
        
        // self.view = videoPreviewView
    }
    
	
	override func viewDidLoad() {
		super.viewDidLoad()
        
        /*** OpenGL preview ***/
        glContext = EAGLContext(api: .openGLES2)
        
        glView.context = glContext!
        glView.drawableDepthFormat = .format24
        // glView.transform = CGAffineTransform(rotationAngle: CGFloat(M_PI_2))
        glView.transform = CGAffineTransform(translationX: 80, y: 0)
        glView.transform = glView.transform.rotated(by: CGFloat(M_PI_2))
        glView.transform = glView.transform.scaledBy(x: 1, y: 1)
        if let window = glView.window {
            glView.frame = window.bounds
        }
        
        ciContext = CIContext(eaglContext: glContext!)
        cameraController = CameraController(previewType: .manual, delegate: self)
        /**********************/
        
        /*** AVCaptureVideoPreviewLayer ***/
//        cameraController = CameraController(previewType: .previewLayer, delegate: self)
//		let previewLayer = cameraController.previewLayer
//		previewLayer?.frame = videoPreviewView.bounds
//		videoPreviewView.layer.addSublayer(previewLayer!)
        /**********************************/
		
		cameraController.registerObserver(self, property: CameraControlObservableSettingAdjustingFocus)
		cameraController.registerObserver(self, property: CameraControlObservableSettingAdjustingWhiteBalance)
		cameraController.registerObserver(self, property: CameraControlObservableSettingAdjustingExposure)
		cameraController.registerObserver(self, property: CameraControlObservableSettingLensPosition)
		cameraController.registerObserver(self, property: CameraControlObservableSettingISO)
		cameraController.registerObserver(self, property: CameraControlObservableSettingExposureDuration)
		cameraController.registerObserver(self, property: CameraControlObservableSettingExposureTargetOffset)
		cameraController.registerObserver(self, property: CameraControlObservableSettingWBGains)
        
        serverController = ServerController(host: "http://ec2-54-194-13-254.eu-west-1.compute.amazonaws.com")
        
        // Start long-polling as soon as the app loads
        self.serverController.longPollServer(serverReturn: processLongPoll)
    }

	
	override func viewDidLayoutSubviews() {
		super.viewDidLayoutSubviews()
		
        /*** AVCaptureVideoPreviewLayer ***/
//		let previewLayer = cameraController.previewLayer
//		previewLayer?.frame = videoPreviewView.bounds
        /**********************************/
	}

	
	override func viewWillAppear(_ animated: Bool) {
		super.viewWillAppear(animated)

		cameraController.startRunning()
	}
    
    override func viewWillDisappear(_ animated: Bool) {
        super.viewWillDisappear(animated)
        
        cameraController.stopRunning()
    }
	
	
	override var prefersStatusBarHidden : Bool {
		return true
	}
	
	
	override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
		
		if let controlsSegue = segue as? ControlsSegue {
			
			controlsSegue.currentViewController = currentControlsViewController
			controlsSegue.hostView = controlsView
			currentControlsViewController = controlsSegue.destination as? UIViewController
			if let currentControlsViewController = currentControlsViewController as? CameraControlsViewControllerProtocol {
				currentControlsViewController.cameraController = cameraController!
			}
		}
	}
	
	
	override func shouldPerformSegue(withIdentifier identifier: String?, sender: Any?) -> Bool {
		return true
	}
	
    // MARK: Other
    /**
        Captures the CIImage currently visible on the screen.
     
        - Returns:
            The filtered CIImage currently being displayed.
    */
    func captureCurrentCIImage() -> CIImage {
        // Reset the current image
        currentCIImage = nil
        // Tell the camera delegate to capture
        shouldCaptureCurrentCIImage = true
        
        // Wait until we've captured the image
        while (currentCIImage == nil) {
            // Do nothing
        }
        
        // Camera delegate deasserts shouldCaptureCurrentImage
        
        return currentCIImage
    }
    
    /**
        Sends a captured UIImage to the server.
     
        - Parameter image: The UIImage to send to the server.s
    */
    func sendImageToServer(image: UIImage) {
        // Stop long-polling
        serverController.cancelLongPollRequest()
        
        // Filter image
        let backgroundQueue = DispatchQueue(label: "com.queue.CameraViewController.background", qos: .background, target: nil)
        
        backgroundQueue.async {
            
            let beginImage = CIImage(image: image)
            let f1 = beginImage?.filterBW(brightness: 0.5, contrast: 2.0)
            
            // TODO: SLIDERS FOR THESE
            let finalImage = f1?.thresholded(min: 0.35, max: 0.8)
            
            // print("finalImage: \(finalImage.)")
            // Upload image
            // self.serverController.uploadUIImageToServerAsJPEG(image: finalUIImage)
            self.serverController.uploadCIImageToServerAsJPEG(ciContext: self.ciContext!, image: finalImage!)
            
            self.serverController.longPollServer(serverReturn: self.processLongPoll)
        }
    }
    
    /**
        Processes a long-poll response and body.
     
        - Parameters:
            - response: The response from github
            - body: The body of the response
     
        - Returns: True if should long-poll again, False if should stop.
    */
    func processLongPoll(response: HTTPURLResponse?, body: Data?) -> Bool {
        guard response != nil else {
            print("Response was nil! Stopping long-polling.")
            return false
        }
        
        guard body != nil else {
            print("Long-polling body was nil! Stopping long-polling.")
            return false
        }
        
        guard self.shouldContinueLongPolling else {
            print("Should not continue long-polling.")
            return false
        }
        
        
        // Time-out occurred, restart long-polling
        if response!.statusCode == 204 {
            return true
            // There's an action for us to do
        } else if response!.statusCode == 200 {
            print("Response code 200. Let's do stuff")
            let utf8Text = String(data: body!, encoding: .utf8)
            print("Response body: \(utf8Text!)")
            
            switch utf8Text! {
            case "takePicture":
                self.cameraController.captureStillImage { image, metadata in
                    self.sendImageToServer(image: image)
                }
                break
            default:
                return false
            }
        
            return true
        }
        
        return false
    }
	
	// MARK: - Actions

	@IBAction func controlButtonPressed(_ sender: UIButton) {
		
		if sender.isSelected {
			sender.isSelected = false
			controlsView.isHidden = true
		}
		else {
			var segueIdentifier : String?
			switch sender {
			case focusButton:
				segueIdentifier = "Embed Focus"
			case exposureButton:
				segueIdentifier = "Embed Exposure"
			case whiteBalanceButton:
				segueIdentifier = "Embed White Balance"
			case optionsButton:
				segueIdentifier = "Embed Options"
			default:break
			}
			
			for button in [focusButton, exposureButton, whiteBalanceButton, optionsButton] {
				button?.isSelected = sender == button
			}
			
			controlsView.isHidden = false
            
            guard segueIdentifier != nil else
            {
                return
            }
            
            self.performSegue(withIdentifier: segueIdentifier!, sender: self)
		}
	}
	
	
	@IBAction func handleShutterButton(_ sender: UIButton) {
		cameraController.captureStillImage { (image, metadata) -> Void in
            
//            let beginImage = CIImage(image: image)
//            let f1 = beginImage?.filterBW(brightness: 0.5, contrast: 2.0)
//            let finalImage = f1?.thresholded(min: 0.35, max: 0.8)
//            
//            self.view.layer.contents = UIImage(ciImage: finalImage!)
//            
//            UIImageWriteToSavedPhotosAlbum(UIImage(ciImage: finalImage!), nil, nil, nil)
            
            self.view.layer.contents = image
            
            self.sendImageToServer(image: image)
            UIImageWriteToSavedPhotosAlbum(image, nil, nil, nil)
		}
	}
	
	
	@IBAction func focusOnPointOfInterest(_ sender: UITapGestureRecognizer) {
		if sender.state == UIGestureRecognizerState.ended {
			var point = sender.location(in: sender.view)
			cameraController.lockFocusAtPointOfInterest(point)
		}
	}
	
	
	// MARK: Camera values observation
	
	func cameraSetting(_ setting: String, valueChanged value: AnyObject) {
		switch setting {
		case CameraControlObservableSettingAdjustingFocus:
			if let adjusting = value as? Bool {
				adjustingFocusIndicator.isHidden = !adjusting
			}
		case CameraControlObservableSettingAdjustingWhiteBalance:
			if let adjusting = value as? Bool {
				adjustingWhiteBalanceIndicator.isHidden = !adjusting
			}
		case CameraControlObservableSettingAdjustingExposure:
			if let adjusting = value as? Bool {
				adjustingExposureIndicator.isHidden = !adjusting
			}
		case CameraControlObservableSettingLensPosition,
			CameraControlObservableSettingExposureTargetOffset,
			CameraControlObservableSettingExposureDuration,
			CameraControlObservableSettingISO,
			CameraControlObservableSettingWBGains:

			displayCurrentValues()
			
		default: break
		}
	}
	
}

// MARK: - CameraControllerDelegate
extension CameraViewController : CameraControllerDelegate {
    
	func cameraController(_ cameraController: CameraController, didDetectFaces faces: Array<(id: Int, frame: CGRect)>) {

		prepareFaceViews(faces.count - faceViews.count)

		for (idx, face) in faces.enumerated() {
			faceViews[idx].frame = face.frame
		}
	}
    
    func cameraController(_ cameraController: CameraController, didOutputImage image:
        CIImage) {
        
        if glContext != EAGLContext.current() {
            EAGLContext.setCurrent(glContext)
        }
        
        glView.bindDrawable()
        
        // print("image.extent.x = \(image.extent.origin.x)\timage.extent.y = \(image.extent.origin.y)")
        // print("image.extent.width = \(image.extent.width)\timage.extent.height = \(image.extent.height)")
        // Live filter
        let f1 = image.filterBW(brightness: 0.5, contrast: 2.0)
        
        // TODO: SLIDERS FOR THESE
        let finalImage = f1.thresholded(min: 0.35, max: 0.8)
        ciContext?.draw(finalImage, in: finalImage.extent, from: finalImage.extent)
        
        
        // Should we save the current image?
        if (shouldCaptureCurrentCIImage) {
            currentCIImage = finalImage
            shouldCaptureCurrentCIImage = false
        }
        
        glView.display()
    }

}


private extension CameraViewController {
	
	func prepareFaceViews(_ diff:Int) {
		if diff > 0 {
			for _ in 0..<diff {
				let faceView = UIView(frame: CGRect.zero)
				faceView.backgroundColor = UIColor.clear
				faceView.layer.borderColor = UIColor.yellow.cgColor
				faceView.layer.borderWidth = 3.0
				facesView.addSubview(faceView)
				
				faceViews.append(faceView)
			}
		}
		else {
			for _ in 0..<abs(diff) {
				faceViews[0].removeFromSuperview()
				faceViews.remove(at: 0)
			}
		}
	}

	
	func displayCurrentValues() {
		var currentValuesTextComponents = [String]()
		
		if let lensPosition = cameraController.currentLensPosition() {
			currentValuesTextComponents.append(String(format: "F: %.2f", lensPosition))
		}
		
		if let offset = cameraController.currentExposureTargetOffset() {
			currentValuesTextComponents.append(String(format: "±: %.2f", offset))
		}

		if let speed = cameraController.currentExposureDuration() {
			currentValuesTextComponents.append(String(format: "S: %.4f", speed))
		}

		if let iso = cameraController.currentISO() {
			currentValuesTextComponents.append(String(format: "ISO: %.0f", iso))
		}
		
		if let temp = cameraController.currentTemperature() {
			currentValuesTextComponents.append(String(format: "TEMP: %.0f", temp))
		}

		if let tint = cameraController.currentTint() {
			currentValuesTextComponents.append(String(format: "TINT: %.0f", tint))
		}

        currentValuesLabel.text = currentValuesTextComponents.joined(separator: " - ")
	}
	
}
