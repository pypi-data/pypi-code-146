from ia.gaius.prediction_models import prediction_ensemble_model_classification, hive_model_classification


class Tester:

    def __init__(self, **kwargs):
        self.bottle = kwargs['bottle']
        self.learning_strategy = kwargs['learning_strategy']

    def next_test_prep(self):
        "Anything to reset in between multiple test runs."
        return

    def train(self, sequence):
        record = {'phase': 'training'}
        historical_expecting = sequence[-1]["strings"][-1]  # Will use the last string object in the last event.
        record['historical_expecting'] = historical_expecting
        self.bottle.clear_wm()
        for data in sequence[:-1]:  # Hold back the last event since it should have the classification.
            if data["vectors"] or data["strings"] or data["emotives"]:
                self.bottle.observe(data)
        self.bottle.observe_classification(sequence[-1])  # Now, we want all the query nodes to get the classification.
        self.bottle.learn()
        return record

    def test(self, sequence):
        record = {'phase': 'testing'}
        historical_expecting = sequence[-1]["strings"][-1]  # Will use the last string object in the last event.
        record['historical_expecting'] = historical_expecting
        self.bottle.clear_wm()
        for data in sequence[:-1]:  # hold back the last event in the sequence because it contains the answer! Give to all query nodes later.
            if data["vectors"] or data["strings"] or data["emotives"]:
                self.bottle.observe(data)

        record['node_predictions'] = {}
        predicton_error = True  ## TODO: If any of the nodes are right, then don't bother learning if on_error learning strategy is employed.

        ensembles = self.bottle.get_predictions()
        for node, ensemble in ensembles.items():
            # Here's where we model
            predicted_value = prediction_ensemble_model_classification(ensemble)
            record['node_predictions'][node] = predicted_value

        hive_prediction = hive_model_classification(ensembles)
        record['node_predictions']['hive'] = hive_prediction
        if hive_prediction == historical_expecting:
            predicton_error = False

        if self.learning_strategy == 'continuous' or (self.learning_strategy == 'on-error' and predicton_error):
            # NOTE!: Now, we're sending the class to the EGRESS nodes for them to learn it, too.
            # Now use the last event.
            self.bottle.observe_classification(
                sequence[-1])  # Now, we want all the query nodes to get the classification.
            self.bottle.learn()
        return record
