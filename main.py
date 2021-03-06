from perceptron import isFace, perceptronFaceClassifierTrainer, whichDigit, perceptronDigitClassifierTrainer
from naiveBayes import isFaceBayes, whichDigitBayes, featureProbMatrixGen
from nearestNeighbors import NNClassifier
import pickle
from statistics import stdev, mean
import matplotlib.pyplot as py
import math
from utils import featureVector

faces = pickle.load(open("faces_dataset", "rb"))
digits = pickle.load(open("digits_dataset", "rb"))

def testNNFaces():
	accuracy = []
	for imageSetLength in range(int(len(faces.trainData) * 0.1), len(faces.trainData), int(len(faces.trainData) * 0.1)):
		numcorrect = 0
		numtotal = len(faces.testData)
		trainFeatureVectors = []
		for i in faces.trainData[0:imageSetLength]:
			trainFeatureVectors.append(featureVector(i.image, 7, 6, 70, 60))
		for i in range(0, numtotal):
			prediction = NNClassifier(faces.testData[i],  faces.trainData[0:imageSetLength], trainFeatureVectors, 7, 6, 70, 60)
			reality = faces.testData[i].label
			if int(prediction) == int(reality):
				numcorrect += 1
		accuracy.append((numcorrect / numtotal))
	return accuracy

def testNNDigits():
	accuracy = []
	for imageSetLength in range(int(len(digits.trainData) * 0.1), len(digits.trainData), int(len(digits.trainData) * 0.1)):
		numcorrect = 0
		numtotal = int(len(digits.testData) * 0.10)
		trainFeatureVectors = []
		for i in digits.trainData[0:imageSetLength]:
			trainFeatureVectors.append(featureVector(i.image, 4, 14, 28, 28))
		for i in range(0, numtotal):
			prediction = NNClassifier(digits.testData[i],  digits.trainData[0:imageSetLength], trainFeatureVectors, 4, 14, 28, 28)
			reality = digits.testData[i].label
			if int(prediction) == int(reality):
				numcorrect += 1
		accuracy.append((numcorrect / numtotal))
	numcorrect = 0
	numtotal = int(len(digits.testData) * 0.10)
	trainFeatureVectors = []
	for i in digits.trainData:
		trainFeatureVectors.append(featureVector(i.image, 4, 14, 28, 28))
	for i in range(0, numtotal):
		prediction = NNClassifier(digits.testData[i], digits.trainData, trainFeatureVectors, 4, 14, 28, 28)
		reality = digits.testData[i].label
		if int(prediction) == int(reality):
			numcorrect += 1
	accuracy.append((numcorrect / numtotal))
	return accuracy

def testPerceptronFaces():
	accuracy = []
	for imageSetLength in range(int(len(faces.trainData) * 0.1), len(faces.trainData), int(len(faces.trainData) * 0.1)):
		weights = perceptronFaceClassifierTrainer(faces.trainData[0:imageSetLength])
		numcorrect = 0
		numtotal = len(faces.testData)
		for i in range(0, numtotal):
			prediction = isFace(faces.testData[i], weights)
			reality = faces.testData[i].label
			if int(prediction) == int(reality):
				numcorrect += 1
		accuracy.append(numcorrect / numtotal)
	return accuracy

def testPerceptronDigits():
	accuracy = []
	trainingData = digits.trainData
	for imageSetLength in range(int(len(trainingData) * 0.1), len(trainingData), int(len(trainingData) * 0.1)):
		weights = perceptronDigitClassifierTrainer(trainingData[0:imageSetLength])
		numcorrect = 0
		numtotal = int(len(digits.testData) * 0.10)
		for i in range(0, numtotal):
			prediction = whichDigit(digits.testData[i], weights)
			reality = digits.testData[i].label
			if int(prediction) == int(reality):
				numcorrect += 1
		accuracy.append((numcorrect / numtotal))
	weights = perceptronDigitClassifierTrainer(trainingData)
	numcorrect = 0
	numtotal = int(len(digits.testData) * 0.10)
	for i in range(0, numtotal):
		prediction = whichDigit(digits.testData[i], weights)
		reality = digits.testData[i].label
		if int(prediction) == int(reality):
			numcorrect += 1
	accuracy.append((numcorrect / numtotal))
	return accuracy

def testNaiveBayesFace():
	accuracy = []
	for imageSetLength in range(int(len(faces.trainData) * 0.1), len(faces.trainData), int(len(faces.trainData) * 0.1)):
		numcorrect = 0
		numtotal = len(faces.testData)
		matrixVector = featureProbMatrixGen(10, 10, 2, A=70, Y=60, trainData= faces.trainData[0:imageSetLength])
		for i in range(0, numtotal):
			prediction = isFaceBayes(faces.testData[i], faces.trainData[0:imageSetLength], matrixVector, 10, 10)
			reality = faces.testData[i].label
			if int(prediction) == int(reality):
				numcorrect += 1
		accuracy.append((numcorrect / numtotal))
	return accuracy

def testNaiveBayesDigits():
	accuracy = []
	for imageSetLength in range(int(len(digits.trainData) * 0.1), len(digits.trainData), int(len(digits.trainData) * 0.1)):
		numcorrect = 0
		numtotal = int(len(digits.testData) * 0.10)
		matrixVector = featureProbMatrixGen(14, 7, 10, A=28, Y=28, trainData= digits.trainData[0:imageSetLength])
		for i in range(0, numtotal):
			prediction = whichDigitBayes(digits.testData[i], digits.trainData[0:imageSetLength], matrixVector, 14, 7)
			reality = digits.testData[i].label
			if int(prediction) == int(reality):
				numcorrect += 1
		accuracy.append((numcorrect / numtotal))
	# to catch the 100%
	numcorrect = 0
	numtotal = int(len(digits.testData) * 0.10)
	matrixVector = featureProbMatrixGen(14, 7, 10, A=28, Y=28, trainData= digits.trainData)
	for i in range(0, numtotal):
		prediction = whichDigitBayes(digits.testData[i], digits.trainData, matrixVector, 14, 7)
		reality = digits.testData[i].label
		if int(prediction) == int(reality):
			numcorrect += 1
	accuracy.append((numcorrect / numtotal))
	return accuracy

def graphAccuracy(algType, dataType, numberOfRuns):
	accuracies = []
	if dataType == 'Face':
		if algType == 'Perceptron':
			accuracies = [testPerceptronFaces() for i in range(0, numberOfRuns)]
		elif algType == 'Naive Bayes':
			accuracies = [testNaiveBayesFace() for i in range(0, numberOfRuns)]
		else:
			accuracies = [testNNFaces() for i in range(0, numberOfRuns)]
	else:
		if algType == 'Perceptron':
			accuracies = [testPerceptronDigits() for i in range(0, numberOfRuns)]
		elif algType == 'Naive Bayes':
			accuracies = [testNaiveBayesDigits() for i in range(0, numberOfRuns)]
		else:
			accuracies = [testNNDigits() for i in range(0, numberOfRuns)]

	std = []
	m = []
	for i in range(0, len(accuracies[0])):
		iValues = []
		for a in accuracies:
			iValues.append(a[i])
		std.append(stdev(iValues))
		m.append(mean(iValues))

	xaxis = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
	fig, (ax1, ax2) = py.subplots(2, sharex=True)
	fig.suptitle('Accuracy of ' + dataType + ' Classification Using the ' + algType + ' Algorithm')
	ax1.set_ylabel('Mean Accuracy')
	ax2.set_ylabel('Standard Deviation of Accuracy')
	ax2.set_xlabel('% of Training Data Used')
	ax1.plot(xaxis, m)
	ax2.plot(xaxis, std)
	locs, labels = py.xticks() 
	py.xticks(locs, xaxis)
	py.show()

graphAccuracy('Perceptron', 'Digit', 5)