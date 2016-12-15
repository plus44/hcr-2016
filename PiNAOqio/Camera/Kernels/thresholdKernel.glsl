kernel vec4 thresholdKernel (
    sampler src, // Source image
    float min, // Anything below becomes black
    float max // Anything above becomes white
    )
{
    vec4 pixValue;
    vec3 blackThresholded, whiteThresholded;

    // Get the value of the current pixel in the GPU grid
    pixValue = sample(src, samplerCoord(src));

    // rgb < min ? black : rgb
    blackThresholded = compare(pixValue.rgb - vec3(min, min, min), vec3(0.0, 0.0, 0.0), pixValue.rgb);

    // rgb > max ? white : rgb
    whiteThresholded = compare(vec3(max, max, max) - blackThresholded, vec3(1.0, 1.0, 1.0), blackThresholded);

    // Alpha always 1.0
    return vec4(whiteThresholded.r, whiteThresholded.g, whiteThresholded.b, 1.0);
}
