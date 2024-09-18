// Select the source directory
sourceDir = getDirectory("Select the source directory");

// Get a list of all files and folders in the source directory
list = getFileList(sourceDir);

// Sort the list
Array.sort(list);

// Input the starting point of x and y
x = 1280;
y = 830;
delta_x = 280;
delta_y = 275;

x_2 = x + 10;
y_2 = 1375;
delta_x_2 = 285;
delta_y_2= 280;

x_3 = x + 20;
y_3 = 1920;
delta_x_3 = 285;
delta_y_3= 280;

x_4 = x + 860;
y_4 = y + -25;
delta_x_4 = 280;
delta_y_4= 280;

x_5 = x_4 + 15;
y_5 = y_2 + -5;
delta_x_5 = 280;
delta_y_5= 280;

x_6 = x_4 + 20;
y_6 = y_3 + 10;
delta_x_6 = 285;
delta_y_6= 285;
// Save the starting point
starting_point = "x = " + x + "\n" +
         "y = " + y + "\n" +
         "delta_x = " + delta_x + "\n" +
         "delta_y = " + delta_y + "\n" + "\n" +
         "x_2 = " + x_2 + "\n" +
         "y_2 = " + y_2 + "\n" +
         "delta_x_2 = " + delta_x_2 + "\n" +
         "delta_y_2 = " + delta_y_2 + "\n" + "\n" +
         "x_3 = " + x_3 + "\n" +
         "y_3 = " + y_3 + "\n" +
         "delta_x_3 = " + delta_x_3 + "\n" +
         "delta_y_3 = " + delta_y_3 + "\n" + "\n" +
         "x_4 = " + x_4 + "\n" +
         "y_4 = " + y_4 + "\n" +
         "delta_x_4 = " + delta_x_4 + "\n" +
         "delta_y_4 = " + delta_y_4 + "\n" + "\n" + 
         "x_5 = " + x_5 + "\n" +
         "y_5 = " + y_5 + "\n" +
         "delta_x_5 = " + delta_x_5 + "\n" +
         "delta_y_5 = " + delta_y_5 + "\n" + "\n" +   
         "x_6 = " + x_6 + "\n" +
         "y_6 = " + y_6 + "\n" +
         "delta_x_6 = " + delta_x_6 + "\n" +
         "delta_y_6 = " + delta_y_6 + "\n" + "\n";
print(starting_point);

// Write the variations to the file
File.saveString(starting_point, sourceDir + "x_y_delta_point.txt");


// Define a function to process a single file
function processFile(filePath) {
	// Open the file
	open(filePath);
	
	// Choose red channels
	Stack.setDisplayMode("color");
	Stack.setChannel(1);
	
	// Reset ROI manager and results
	roiManager("reset");
	run("Clear Results");
	
	// Define a loop to create and analyze each ROI
	for (i = 1; i <= 6; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x + ((i - 1) % 3) * delta_x;
	    y_roi = y + Math.floor((i - 1) / 3) * delta_y;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    redMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("red region #" + i + " is " + redMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 7; i <= 12; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_2 + ((i - 7) % 3) * delta_x_2;
	    y_roi = y_2 + Math.floor((i - 7) / 3) * delta_y_2;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    redMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("red region #" + i + " is " + redMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 13; i <= 18; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_3 + ((i - 13) % 3) * delta_x_3;
	    y_roi = y_3 + Math.floor((i - 13) / 3) * delta_y_3;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    redMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("red region #" + i + " is " + redMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 19; i <= 24; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_4 + ((i - 19) % 3) * delta_x_4;
	    y_roi = y_4 + Math.floor((i - 19) / 3) * delta_y_4;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    redMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("red region #" + i + " is " + redMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 25; i <= 30; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_5 + ((i - 25) % 3) * delta_x_5;
	    y_roi = y_5 + Math.floor((i - 25) / 3) * delta_y_5;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    redMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("red region #" + i + " is " + redMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 31; i <= 36; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_6 + ((i - 31) % 3) * delta_x_6;
	    y_roi = y_6 + Math.floor((i - 31) / 3) * delta_y_6;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    redMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("red region #" + i + " is " + redMean_i);
	}

	// Show all ROIs in the image
	roiManager("Show All with labels");
	roiManager("measure");
	roiManager("reset");

	// Choose green channels
	Stack.setDisplayMode("color");
	Stack.setChannel(2);

	// Define a loop to create and analyze each ROI
	for (i = 1; i <= 6; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x + ((i - 1) % 3) * delta_x;
	    y_roi = y + Math.floor((i - 1) / 3) * delta_y;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    greenMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("green region #" + i + " is " + greenMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 7; i <= 12; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_2 + ((i - 7) % 3) * delta_x_2;
	    y_roi = y_2 + Math.floor((i - 7) / 3) * delta_y_2;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    greenMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("green region #" + i + " is " + greenMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 13; i <= 18; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_3 + ((i - 13) % 3) * delta_x_3;
	    y_roi = y_3 + Math.floor((i - 13) / 3) * delta_y_3;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    greenMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("green region #" + i + " is " + greenMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 19; i <= 24; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_4 + ((i - 19) % 3) * delta_x_4;
	    y_roi = y_4 + Math.floor((i - 19) / 3) * delta_y_4;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    greenMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("green region #" + i + " is " + greenMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 25; i <= 30; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_5 + ((i - 25) % 3) * delta_x_5;
	    y_roi = y_5 + Math.floor((i - 25) / 3) * delta_y_5;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    greenMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("green region #" + i + " is " + greenMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 31; i <= 36; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_6 + ((i - 31) % 3) * delta_x_6;
	    y_roi = y_6 + Math.floor((i - 31) / 3) * delta_y_6;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    greenMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("green region #" + i + " is " + greenMean_i);
	}

	// Show all ROIs in the image
	roiManager("Show All with labels");
	roiManager("measure");
	roiManager("reset");

	// Choose blue channels
	Stack.setDisplayMode("color");
	Stack.setChannel(3);

	// Define a loop to create and analyze each ROI
	for (i = 1; i <= 6; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x + ((i - 1) % 3) * delta_x;
	    y_roi = y + Math.floor((i - 1) / 3) * delta_y;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    blueMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("blue region #" + i + " is " + blueMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 7; i <= 12; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_2 + ((i - 7) % 3) * delta_x_2;
	    y_roi = y_2 + Math.floor((i - 7) / 3) * delta_y_2;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    blueMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("blue region #" + i + " is " + blueMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 13; i <= 18; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_3 + ((i - 13) % 3) * delta_x_3;
	    y_roi = y_3 + Math.floor((i - 13) / 3) * delta_y_3;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    blueMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("blue region #" + i + " is " + blueMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 19; i <= 24; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_4 + ((i - 19) % 3) * delta_x_4;
	    y_roi = y_4 + Math.floor((i - 19) / 3) * delta_y_4;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    blueMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("blue region #" + i + " is " + blueMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 25; i <= 30; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_5 + ((i - 25) % 3) * delta_x_5;
	    y_roi = y_5 + Math.floor((i - 25) / 3) * delta_y_5;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    blueMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("blue region #" + i + " is " + blueMean_i);
	}
	
	// Define a loop to create and analyze each ROI
	for (i = 31; i <= 36; i++) {
	    // Define the coordinates of the current ROI
	    x_roi = x_6 + ((i - 31) % 3) * delta_x_6;
	    y_roi = y_6 + Math.floor((i - 31) / 3) * delta_y_6;
	    
	    // Create the current ROI and get its mean value
	    makeRectangle(x_roi, y_roi, 100, 100);
	    blueMean_i = getValue("Mean");
	    roiManager("Add");
	    
	    // Print the result for the current ROI
	    print("blue region #" + i + " is " + blueMean_i);
	}

	// Show all ROIs in the image
	roiManager("Show All with labels");
	roiManager("measure");

	// Save the results
	saveAs("Results", filePath + "_RGB.csv");
	
	// Close the file
	close();
}

// Define a function to recursively process all files in a folder
function processFolder(folderPath) {
	// Get a list of all files and folders in the folder
	list = getFileList(folderPath);
	
	// Sort the list
	Array.sort(list);
	
	// Loop over all files and folders in the folder
	for (i = 0; i < list.length; i++) {
		// Construct the full path to the current file or folder
		path = folderPath + list[i];
		
		// If the current item is a file, process it
		if (endsWith(path, ".tiff")) {
			processFile(path);
		}
		
		// If the current item is a folder, recursively process it
		if (File.isDirectory(path)) {
			processFolder(path + "/");
		}
	}
}

// Call the processFolder function on the source directory
processFolder(sourceDir);
