import unittest
from unittest.mock import patch

import paramiko

from Joblib_Estimator_Function.Resume_Training_Ciclo import read_estimator, read_state
from funzioni_script_new import copy_file_to_ec2


class TestMyFunctions(unittest.TestCase):

    def test_read_estimator(self):
        # Test caso in cui il file del modello esiste
        n_estimators = read_estimator('training_state.pkl')
        expected_value = 30
        self.assertEqual(n_estimators, expected_value)  # Verifica che il risultato sia corretto

        # Test caso in cui il file del modello non esiste
        n_estimators = read_estimator('nonexistent_model.pkl')
        self.assertIsNone(n_estimators)  # Verifica che il risultato sia None

    def test_read_state(self):
        # Test caso in cui il file dello stato di addestramento esiste
        n_estimators, X_train, model, X_test, y_test = read_state('training_state.pkl')
        # Verifica che il numero di estimatori sia uguale a 30
        expected_n_estimators = 30
        assert n_estimators == expected_n_estimators, f"Errore: numero di estimatori atteso {expected_n_estimators}, ottenuto {n_estimators}"

        # Verifica che X_train sia un DataFrame non vuoto
        assert not X_train.empty, "Errore: X_train è vuoto"

        # Verifica che il modello sia un'istanza della classe MyModel
        #assert isinstance(model, MyModel), "Errore: il modello non è un'istanza della classe MyModel"

        # Verifica che X_test e y_test non siano vuoti
        assert not X_test.empty, "Errore: X_test è vuoto"
        assert not y_test.empty, "Errore: y_test è vuoto"

        # Test caso in cui il file dello stato di addestramento non esiste
        result = read_state('nonexistent_state.pkl')
        self.assertIsNone(result)  # Verifica che il risultato sia None

        # Test caso in cui si verifica un errore nel caricamento dello stato di addestramento
        result = read_state('corrupted_state.pkl')
        self.assertIsNone(result)  # Verifica che il risultato sia None




if __name__ == '__main__':
    unittest.main()