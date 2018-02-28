# Adaptive Backlight

Control an LED strip to illuminate the space behind a computer monitor. 

Individually-addressable LEDs adaptively change color according to the distribution of colors on the screen. A modular design permits mixing of software components to generate novel behavior. These components expose a common interface that allows variants to be developed independently.

## Project outline

The software is divided to two parts: controller-side and host-side. The host-side is necessary for complete adaptive functionality but non-adaptive behaviors are possible without the host. 

The controller-side software consists of four main modules and an optional fifth module:

* The `Reader` reads an image and returns a matrix of RGB pixel colors.
* The `Collector` distributes pixel colors to each LED.
* The `Analyzer` aggregates a collection of pixel colors to a color for each LED.
* The `Controller` drives a hardware or software device to reproduce the final color for each LED.
* The `Viewer` (optional) displays the color of each LED on the screen (for example, for testing).

The host-side software runs a minimal web server that captures a screenshot and returns image data  to the controller upon request.

## Controller-side modules

### Reader

The `Reader` reads image data from a variety of sources and must return an $M\timesN\times3$ RGB matrix. Here are some example implementations of `Reader`: 

* FileReader: reads image data from a path on a mounted file system. The image data may or may not change.
* HTTPReader: pings a webserver to request an image, usually a screenshot of the host computer's desktop.
* StaticColorReader: returns 'fake' image data consisting of a single RGB array. This can be used to set a uniform color on all LEDs.

### Collector

The `Collector` groups RGB data and distributes it to the LEDs. For example, it may assign RGB data from the top-left corner of the screen to the top-most and left-most LED behind the monitor. There are many ways to decide how to partition the image data to the LEDs.

A pleasant, but slow, implementation (`VoronoiCollector`) takes advantage of Voronoi cells to segment the screen using the physical positions of the LEDs. Briefly, each pixel on the screen gets assigned to the $k$ nearest LEDs. Higher values of $k$ increase mixing of the on-screen colors; $k=1$ assigns each pixel to exactly one LED, leading to the sharpest differences in LED colors.

The `Collector` returns a dictionary of RGB value arrays.

### Analyzer

The `Analyzer` decides what each LED should do with its distribution of RGB values. Two simple examples are:

* MeanAnalyzer: takes the mean of over all RGB values for each color channel.
* MedianAnalyzer: takes the median value over all RGB values for each color channel.

The `Analyzer` returns a dictionary of RGB tuples.

### Controller

The `Controller` drives a software or hardware device with appropriate instructions. There are two controller implementations: 

* WS281xController: drives the popular *WS281X* LED strip using the `neopixel` library.
* MatplotlibController: drives the `MatplotlibViewer` to display simulations of LED colors. This is useful for developing and testing.

The output of the `Controller`, if any, depends on the `Viewer` variant it connects to. The viewer component, however, is not necessary; in this case, the `Controller` is the last stage of the main loop.

### Viewer

At the moment, only the `MatplotlibViewer` variant is implemented. It displays a continuously-refreshing plot showing simulated LED colors.

## Server-side components

Server-side components are required for adaptive control but are otherwise optional.

The current implementation offers a minimal web-server that captures and returns the host computer's desktop contents. This can be combined with the `HTTPReader` variant of the controller-side `Reader` module, which pings the web-server when a new input image is required. It is also possible to point to a web-server that is running on a machine *other* than the host machine.


