//
//  ServerController.swift
//  PiNAOqio
//
//  Created by Mihnea Rusu on 06/12/16.
//  Copyright © 2016 Mihnea Rusu. All rights reserved.
//

import Foundation
import Alamofire
import SwiftyJSON
import UIKit

class ServerController : NSObject {
    
    var host : String!
    var port : Int!
    var url : String!
    var isLongPolling : Bool = false
    var jsonPost = JSON(["doneTakingPicture" : nil, "error" : nil, "picture" : nil, "format" : nil])
    weak var longPollRequest : Request?
    
    let queue  = DispatchQueue(label: "com.queue.ServerController.Serial")
    
    init(host: String) {
        super.init()
        
        self.host = host
        self.port = 80
        self.url = "\(host):\(port)/phone"
    
    }
    
    /**
        Resets the values of the keys in jsonPost.
    */
    func resetJsonPost() {
        jsonPost["doneTakingPicture"].bool = false
        jsonPost["error"].string = "NotInitialized"
        jsonPost["picture"].string = nil
        jsonPost["format"].string = nil
    }
    
    /**
        Cancels the on-going long-poll request.
    */
    func cancelLongPollRequest() {
        longPollRequest?.cancel()
        print("Cancelled long-poll request.")
    }
    
    /**
        Long polls the host:port combination at /phone with a GET request.
     
        - Parameters:
            - serverReturn: A callback that gets triggered when the server has responded. Should return true if the long-polling is to continue, or false if the long-polling is to stop (will need to be manually queued afterwards).
            - response: The response header from the server.
            - body: The raw data in the server response.
     */
    func longPollServer(serverReturn: @escaping (_ response: HTTPURLResponse?, _ body: Data?) -> Bool) {
        
        print("Starting long-polling.")
        longPollRequest = Alamofire.request(url, method: .get)
            .response { response in
                
                if serverReturn(response.response, response.data) {
                    self.longPollServer(serverReturn: serverReturn)
                } else {
                    self.longPollRequest = nil
                }
            } // end of response closure
    }
    
    /**
        Uploads a CIImage to the server at /phone using a POST request, under the "picture" entry in the JSON dictionary.
     
        - Parameters:
            - ciContext: A CIContext object that can be used to convert the CIImage to JPEG.
            - image: Image to send
    */
    func uploadCIImageToServerAsJPEG(ciContext: CIContext, image: CIImage) {
        queue.sync {
            if let jpegImage = ciContext.jpegRepresentation(of: image, colorSpace: CGColorSpace(name: CGColorSpace.genericRGBLinear)!, options: ["kCGImageDestinationLossyCompressionQuality" : 0.9]) {
                
                jsonPost["doneTakingPicture"].bool = true
                jsonPost["error"].string = "None"
                jsonPost["picture"].string = jpegImage.base64EncodedString(options: .lineLength64Characters)
                jsonPost["format"].string = "jpeg"
            } // end of if let jpegImage
        } // end of queue.sync
        
        postJSONPostToServer()
    } // end of func uploadImageToServerAsJpeg
    
    /**
        Uploads a UIImage to the server at /phone using a POST request, under the "picture" entry in the JSON dictionary.
     
        - Parameter image: The image to upload as JPEG.
    */
    func uploadUIImageToServerAsJPEG(image: UIImage) {
        queue.sync {
            if let jpegImage = UIImageJPEGRepresentation(image, 0.5) {
                jsonPost["doneTakingPicture"].bool = true
                jsonPost["error"].string = "None"
                jsonPost["picture"].string = jpegImage.base64EncodedString(options: .lineLength64Characters)
                jsonPost["format"].string = "jpeg"
                
                print("Converted image to JPEG!")
            } // end of if let jpegImage
        } // end of queue.sync
        
        postJSONPostToServer()
    }
    
    /** 
        Uploads a UIImage to the server under the "picture" entry in the JSON dictionary at the /phone address of the server host.
     
        - Parameter image: The image to upload as PNG.
    */
    func uploadUIImageToServerAsPNG(image: UIImage) {
        queue.sync {
            if let pngImage = UIImagePNGRepresentation(image) {
                jsonPost["doneTakingPicture"].bool = true
                jsonPost["error"].string = "None"
                jsonPost["picture"].string = pngImage.base64EncodedString(options: .lineLength64Characters)
                jsonPost["format"].string = "png"
            } // end of if let pngImage
        } // end of queue.sync
        
        postJSONPostToServer()
    }
    
    /**
        Posts the JSON post instance variable to the server at the /phone address on the host.
    */
    private func postJSONPostToServer() {
        let headers : HTTPHeaders = [
            "Content-type" : "application/json"
        ]
        
        do {
            let jsonString = try jsonPost.rawData(options: .prettyPrinted)
            print("jsonString rawData: \(jsonString)")
            
            // Upload to server
            Alamofire.upload(jsonString, to: url, method: .post, headers: headers)
                .response { response in
                    
                    self.resetJsonPost()
                    
                    if response.response?.statusCode == 200 {
                        print("Successfully POSTed JSON to server.")
                    } else {
                        print("Failed POSTing JSON to server.")
                        print("Status code received: \(response.response?.statusCode)")
                    }
            }
        } catch {
            print("Failed converting jsonString to rawData")
        }

    }
    
}
