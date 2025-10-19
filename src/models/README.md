# Models used in the data analysis


### dummy_methods.py

Is an example of a possible class we could define for the project (Object-Oriented Programming), just to have the structure of how we should define the model classes. In the different python files (probably the scripts.py) file, we should refer it as this :\


from src.models.dummy_methods import DummyClassifier

1. Instanciate the object with the chosen class\
method_obj = DummyClassifier(arg1, arg2)

2. Fit (:=train) the method on the training data\
preds_train = method_obj.fit(xtrain, ytrain)

3. Predict on unseen data\
preds = method_obj.predict(xtest)




# Contained elements
- DataPreparation.ipynb: clean the initial data (ex: newyorker caption database), then save it in src/data/dataPrepared.pkl
- gui.py: tiny window to select and display all stored plots in plots_gui.pkl
- plots_gui.py: class defintion for plot-obects(store additional info about the plot + useful methods such as show the plot or save/load plots)


Model definitions and training logic.
- some_model.py defining neural nets, regressors, etc.  - Code for model initialization, loss, optimizer, forward pass.
