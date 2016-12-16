 # USAGE
# python compare.py

# import the necessary packages
from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)

	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))

	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap = plt.cm.gray)
	plt.axis("off")

	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap = plt.cm.gray)
	plt.axis("off")

	# show the images
	plt.show()

# load the images -- the original, the original + contrast,
# and the original + photoshop
original = cv2.imread("original_image.jpg")
compare_1 = cv2.imread("similar_Images/image11.jpg")
compare_2 = cv2.imread("similar_Images/image2.jpg")
compare_3 = cv2.imread("similar_Images/image3.jpg")


# convert the images to grayscale
original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
compare_1 = cv2.cvtColor(compare_1, cv2.COLOR_BGR2GRAY)
compare_2 = cv2.cvtColor(compare_2, cv2.COLOR_BGR2GRAY)
compare_3 = cv2.cvtColor(compare_3, cv2.COLOR_BGR2GRAY)

# initialize the figure
fig = plt.figure("Images")
images = ("Original", original), ("Image1", compare_1), ("Image2", compare_2), ("Image3", compare_3)

# loop over the images
for (i, (name, image)) in enumerate(images):
	# show the image
	ax = fig.add_subplot(1, 4, i + 1)
	ax.set_title(name)
	plt.imshow(image, cmap = plt.cm.gray)
	plt.axis("off")

# show the figure
# plt.show()

# compare the images
# compare_images(original, original, "Original vs. Original")
compare_images(original, compare_1, "Original vs. Image1.png")
compare_images(original, compare_2, "Original vs. Image2.png")
compare_images(original, compare_3, "Original vs. Image3.png")