import numpy as np
from .abstract_ranker import AbstractRanker
import pandas as pd
from fair_dynamic_rec.core.util.outputs import make_output_dir
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import os.path

class NeighborUCB1(AbstractRanker):
    def __init__(self, config, dataObj, parameters=None):
        super(NeighborUCB1, self).__init__(config, dataObj)
        self.n_samples = np.zeros(dataObj.n_users)
        self.n_clicks = np.zeros(dataObj.n_users)
        self.prng = np.random.RandomState(seed=config.seed)
        self.sigma = float(parameters["sigma"]["value"]) if "sigma" in parameters else 1.0

        self.l = int(parameters["latent_dim"]["value"]) if "latent_dim" in parameters else 0
        self.lambda_1 = float(parameters["lambda"]["value"]) if "lambda" in parameters else 1.0
        self.alpha_v = float(parameters["alpha_v"]["value"]) if "alpha_v" in parameters else 1.0
        self.alpha_u = float(parameters["alpha_u"]["value"]) if "alpha_u" in parameters else 1.0
        self.noise = float(parameters["noise"]["value"]) if "noise" in parameters else 0.00001

        self.X = dataObj.train_data
        self.X = (self.X > 0).astype(float)
        self.X = self.X + self.noise

        self.XTX = np.dot(self.X.T, self.X)

        self.U = np.zeros((self.dataObj.n_items, self.l)) + self.noise
        self.V = np.zeros((self.dataObj.n_items, self.l)) + self.noise

        # A = U_T * (X_T.X + lambda) * U      -> l * l
        self.A = np.eye(self.l)
        self.AInv = np.linalg.inv(self.A)

        # U_T * (X_T . X_{u,i} - dMat(\etha))   -> l * m
        self.b = np.zeros((self.l, dataObj.n_items))

        # X_T . X + \lambda                   -> m * m
        self.C = self.XTX + self.lambda_1 * np.eye(dataObj.n_items)
        self.CInv = np.linalg.inv(self.C)

        # (X_T . X + dMat(\etha)) * V          -> m * l
        self.d = np.zeros((dataObj.n_items, self.l))

        self.E = np.eye(self.l)
        self.EInv = np.linalg.inv(self.E)

        self.writeSimMat()

        # self.ill_matrix_counter = 0
        # # for ill inverse
        # self.AInv_tmp = np.zeros((self.dataObj.n_users, (self.k + self.l) * self.dataObj.n_users, (self.k + self.l) * self.dataObj.n_users))
        # self.b_tmp = np.zeros((self.dataObj.n_users, (self.k + self.l) * self.dataObj.n_users))
        # self.CInv_tmp = np.zeros((self.dataObj.n_items, self.l, self.l))
        # self.d_tmp = np.zeros((self.dataObj.n_items, self.l))

    def get_ranking(self, batch_users, sampled_items=None, round=None):
        """
        :param x: features
        :param k: number of positions
        :return: ranking: the ranked item id.
        """
        # assert x.shape[0] >= k
        rankings = np.zeros((len(batch_users), self.config.list_size), dtype=int)
        # self.batch_features = np.zeros((len(batch_users), self.config.list_size, self.dim))
        tie_breaker = self.prng.rand(self.dataObj.n_items)
        for i in range(len(batch_users)):
            user = batch_users[i]

            user_vector = np.reshape(self.X[user], (1,self.X.shape[1]))

            score = np.dot(self.X[user], np.dot(self.U, self.V.T))
            score[np.isnan(score)] = 0
            XU = np.multiply(user_vector.T,self.U) # 1 * k
            cb1 = np.sqrt(np.sum(np.multiply(np.dot(XU, self.AInv), XU), axis=1))
            cb1[np.isnan(cb1)] = 0
            cb2 = np.sqrt(np.multiply(np.dot(self.X[user], self.CInv), self.X[user]))
            cb2[np.isnan(cb2)] = 0
            cb3 = np.sqrt(np.sum(np.multiply(np.dot(self.V, self.EInv), self.V), axis=1))
            cb3[np.isnan(cb3)] = 0

            ucb = score + self.alpha_u * cb1 + self.alpha_v * cb2 * cb3

            rankings[i] = np.lexsort((tie_breaker, -ucb))[:self.config.list_size]

            self.writeCB(round+i, cb1, cb2, cb3)

        return rankings

    def update(self, batch_users, rankings, clicks, round=None, user_round=None):
        for i in range(len(batch_users)):
            user = batch_users[i]

            _clicks, _ranking = self.__collect_feedback(clicks[i], rankings[i])

            clicked_items = _ranking[np.where(_clicks)[0]]
            X_clicked_items = np.zeros((self.dataObj.n_items, self.dataObj.n_users))
            if sum(_clicks) > 0:
                X_clicked_items[clicked_items, user] = np.ones((len(clicked_items),1))
                # Update XTX
                self.XTX = self.XTX + np.dot(X_clicked_items, self.X)

                # Update C and CInv
                self.C += np.dot(X_clicked_items, self.X)
                self.CInv = np.linalg.inv(self.C)

                # Update X
                self.X[user, clicked_items] += np.ones(len(clicked_items), dtype=float)

            # compute eta for U
            # eta = (np.dot(np.dot(np.dot(np.dot(np.dot(self.C,self.X[user,:].T),self.X[user,:]),self.V[_ranking]),self.E),self.V[_ranking].T)).diagonal() \
            #       / np.divide(self.C[_ranking,_ranking],np.dot(np.dot(self.V[_ranking],self.E),self.V[_ranking].T)).diagonal()
            eta_tmp = (np.dot(np.dot(np.dot(np.dot(np.dot(self.C, self.X.T), self.X), self.V), self.E),self.V.T)).diagonal() \
                  / np.divide(self.C,np.dot(np.dot(self.V, self.E), self.V.T))
            eta_tmp[np.isnan(eta_tmp)] = 0
            eta = np.zeros((self.dataObj.n_items, self.dataObj.n_items))
            eta = np.diag(np.diag(eta_tmp))[_ranking]

            # Update d
            self.d += np.dot((np.dot(self.X[user].T.reshape(self.dataObj.n_items,1), _clicks.reshape(1,len(_clicks))) - eta.T), self.V[_ranking])

            # Update U
            self.U = np.dot(np.dot(self.CInv, self.d), self.EInv)
            self.U = self.U / np.sqrt(np.sum(self.U ** 2))

            #compute eta for V
            # eta = np.dot(np.dot(np.dot(np.dot(self.U, self.AInv), self.U.T), self.X[user].T), X_clicked_items.T[user]).diagonal() \
            #       / np.dot(np.dot(self.U, self.AInv), self.U.T).diagonal()
            eta_tmp = np.dot(np.dot(np.dot(np.dot(self.U, self.AInv), self.U.T), self.X.T), self.X) \
                  / np.dot(np.dot(self.U, self.AInv), self.U.T)
            eta_tmp[np.isnan(eta_tmp)] = 0
            eta = np.diag(np.diag(eta_tmp))[_ranking]

            # Update A
            user_vector = np.reshape(self.X[user], (1, self.X.shape[1]))
            XU = np.multiply(user_vector.T, self.U)  # m * k
            self.A += np.dot(XU.T, XU) + self.lambda_1 * np.dot(self.U.T, self.U)
            try:
                self.AInv = np.linalg.inv(self.A)
            except np.linalg.LinAlgError:
                # for the ill matrix. if the matrix is not invertible, we ignore this update
                print('ill matrix A.')
                self.AInv = np.linalg.pinv(self.A)

            # Update b
            self.b[:, _ranking] += np.dot(self.U.T, (np.dot(self.X[user].T.reshape(self.dataObj.n_items,1), _clicks.reshape(1,len(_clicks))) - eta.T))

            # Update V.T
            self.V[_ranking] = np.dot(self.AInv, self.b[:, _ranking]).T
            # self.V = self.V / np.sqrt(np.sum(self.V ** 2))

            # Update E
            self.E = self.E + np.dot(self.V[_ranking].T, self.V[_ranking])
            self.EInv = np.linalg.inv(self.E)

            # Update U again
            self.U = np.dot(np.dot(self.CInv, self.d), self.EInv)
            self.U = self.U / np.sqrt(np.sum(self.U ** 2))

            self.n_samples[user] += len(_clicks)
            self.n_clicks[user] += sum(_clicks)

            self.writeParams(round)

    def __collect_feedback(self, click, ranking):
        """
        :param y:
        :return: the last observed position.
        """
        # With  Cascade assumption, only the first click counts.
        if self.config.feedback_model == 'cascade':
            if np.sum(click) == 0:
                return click, ranking
            first_click = np.where(click)[0][0]
            return click[:first_click + 1], ranking[:first_click +1]
        elif self.config.feedback_model == 'dcm':
            if np.sum(click) == 0:
                return click, ranking
            last_click = np.where(click)[0][-1]
            return click[:last_click + 1], ranking[:last_click + 1]
        # all items are observed
        else:
            return click, ranking

    def writeCB(self, round, cb1, cb2, cb3):
        f=open('cb1.txt','a')
        f.write(str(round)+'\t'+",".join(map(str, cb1)))
        f.close()

        f = open('cb2.txt', 'a')
        f.write(str(round) + '\t' + ",".join(map(str, cb2)))
        f.close()

        f = open('cb3.txt', 'a')
        f.write(str(round) + '\t' + ",".join(map(str, cb3)))
        f.close()

    def writeParams(self, round):
        if round == 0:
            return
        pre_path = self.config._target / Path('results')
        U_path = pre_path / Path('U'+str(round)+'.txt')
        V_path = pre_path / Path('V'+str(round)+'.txt')

        df = pd.DataFrame(data=self.U.astype(float))
        df.to_csv(U_path, sep=' ', header=False, float_format='%.10f', index=False)

        df = pd.DataFrame(data=self.V.astype(float))
        df.to_csv(V_path, sep=' ', header=False, float_format='%.10f', index=False)

    def writeSimMat(self):
        pre_path = self.config._target

        test_sim_path = pre_path / Path('test_item_sim.txt')
        train_sim_path = pre_path / Path('train_item_sim.txt')
        data_sim_path = pre_path / Path('data_item_sim.txt')

        if not os.path.isfile(test_sim_path):
            item_sim_matrix = cosine_similarity(self.dataObj.test_data.T)
            np.fill_diagonal(item_sim_matrix, 0)
            df = pd.DataFrame(data=item_sim_matrix.astype(float))
            df.to_csv(test_sim_path, sep=' ', header=False, float_format='%.10f', index=False)

        if not os.path.isfile(train_sim_path):
            item_sim_matrix = cosine_similarity(self.dataObj.train_data.T)
            np.fill_diagonal(item_sim_matrix, 0)
            df = pd.DataFrame(data=item_sim_matrix.astype(float))
            df.to_csv(train_sim_path, sep=' ', header=False, float_format='%.10f', index=False)

        if not os.path.isfile(data_sim_path):
            item_sim_matrix = cosine_similarity((self.dataObj.test_data + self.dataObj.train_data).T)
            np.fill_diagonal(item_sim_matrix, 0)
            df = pd.DataFrame(data=item_sim_matrix.astype(float))
            df.to_csv(data_sim_path, sep=' ', header=False, float_format='%.10f', index=False)