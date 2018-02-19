# Adaptive Backlight

## Project outline

Running on the Raspberry Pi:

* Initializer
* Main loop
** Reader
** Analyzer
** Controller
** Viewer (optional)
* Signal interrupt

Running on the host desktop:

* Screenshot capture in cron.

## Components

### Initializer

### Reader

Reads the screenshot bitmap into memory.

Input: $N \times M$ matrix of RGB (3-tuples).
Output: array of RGB tuples for each LED.

### Analyzer

Determines the color of each LED.

Input: array of RGB tuples for each LED.
Output: RGB tuples for each LED.

### Controller

Sends instructions to the LED driver.

Input: RGB tuples for each LED.
Output: instructions sent to driver.

### Viewer

This is an optional viewer to simulate LEDs.

Input: LED driver instructions.
Output: graphical representation of LED colors.

### Capturer

A shell script, probably, that captures the root window on the host desktop as a bitmap.

Output: $N \times M$ matrix of RGB tuples.



