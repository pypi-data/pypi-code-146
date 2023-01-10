import numpy as np
from .abstract_ranker import AbstractRanker
import sys
from sklearn.metrics.pairwise import cosine_similarity

# Objective function: min 1/2 (X - U . V_T) + 1/2 * \lambda (U)^2 + 1/2 * \lambda (V)^2

class FactorUCB(AbstractRanker):
    def __init__(self, config, dataObj, parameters=None):
        super(FactorUCB, self).__init__(config, dataObj)
        self.n_samples = np.zeros(dataObj.n_users)
        self.n_clicks = np.zeros(dataObj.n_users)
        self.prng = np.random.RandomState(seed=config.seed)
        self.sigma = float(parameters["sigma"]["value"]) if "sigma" in parameters else 1.0

        self.l = int(parameters["latent_dim"]["value"]) if "latent_dim" in parameters else 0
        self.lambda_1 = float(parameters["lambda1"]["value"]) if "lambda1" in parameters else 1.0
        self.lambda_2 = float(parameters["labmda2"]["value"]) if "lambda2" in parameters else 1.0
        self.alpha_a = float(parameters["alpha_a"]["value"]) if "alpha_a" in parameters else 1.0
        self.alpha_u = float(parameters["alpha_u"]["value"]) if "alpha_u" in parameters else 1.0
        self.w_type = parameters["w_type"]["value"] if "w_type" in parameters else ""

        self.V = np.zeros((self.dataObj.n_items, self.l))
        self.k = 0
        self.contextual_var = bool(parameters["contextual_variable"]["value"]) if "contextual_variable" in parameters else False
        if self.contextual_var:
            self.X = self.dataObj.feature_data['train_item_topical_features']
            self.k = self.X.shape[1]
            self.XV = np.concatenate((self.X, self.V), axis=1)
            # self.XV_optimal = np.concatenate((self.X, self.dataObj.feature_data['test_item_latent_features']), axis=1)
        else:
            self.XV = self.V
            # self.XV_optimal = self.dataObj.feature_data['test_item_latent_features']
        self.Theta = np.zeros((self.dataObj.n_users, self.k + self.l))
        self.Theta_x = self.Theta[:, :self.k]
        self.Theta_v = self.Theta[:, self.k:]
        self.W = np.identity(n=self.dataObj.n_users)
        if self.w_type == "user-user_sim":
            self.W = cosine_similarity(dataObj.train_data)

        # self.A = np.zeros((self.dataObj.n_users, (self.k+self.l)*self.dataObj.n_users, (self.k+self.l)*self.dataObj.n_users))
        # self.A = np.zeros((self.dataObj.n_users, self.lambda_1 * np.identity(n=(self.k+self.l)*self.dataObj.n_users)))
        self.AInv = np.zeros((self.dataObj.n_users, (self.k+self.l)*self.dataObj.n_users, (self.k+self.l)*self.dataObj.n_users))
        # self.AInv = np.zeros((self.dataObj.n_users, self.lambda_1 * np.identity(n=(self.k + self.l) * self.dataObj.n_users)))
        identity = self.lambda_1 * np.identity(n=(self.k+self.l)*self.dataObj.n_users)
        for i in range(self.AInv.shape[0]):
            # self.A[i] = identity
            self.AInv[i] = np.linalg.inv(identity)  # np.zeros((self.k+self.l,self.k+self.l))
        print("AInv dimensions: " + str(self.AInv.shape))
        sys.stdout.flush()
        self.b = np.zeros((self.dataObj.n_users, (self.k+self.l)*self.dataObj.n_users))

        self.C = np.zeros((self.dataObj.n_items, self.l, self.l))
        self.CInv = np.zeros((self.dataObj.n_items, self.l, self.l))
        for i in range(self.C.shape[0]):
            self.C[i] = self.lambda_2 * np.identity(n=self.l)
            self.CInv[i] = np.linalg.inv(self.C[i])  # np.zeros((self.k+self.l,self.k+self.l))
        print("C dimensions: " + str(self.C.shape) + ", " + str(self.CInv.shape))
        sys.stdout.flush()
        self.d = np.zeros((self.dataObj.n_items, self.l))

        self.ill_matrix_counter = 0
        # for ill inverse
        # self.AInv_tmp = np.zeros((self.dataObj.n_users, (self.k+self.l)*self.dataObj.n_users, (self.k+self.l)*self.dataObj.n_users))
        # self.b_tmp = np.zeros((self.dataObj.n_users, (self.k+self.l)*self.dataObj.n_users))
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
        tie_breaker = self.prng.rand(len(sampled_items))
        for i in range(len(batch_users)):
            user = batch_users[i]

            # compute vec((X_a_t,V_a_t)W^T) -> N * (k+l)N
            XVW = self.create_vectorized_matrix(self.W.shape[0], self.W.shape[0]*(self.k+self.l), self.XV, self.W, range(len(sampled_items)))

            # compute line 9 of Algorithm 1
            score = np.dot(self.XV[sampled_items], np.dot(self.Theta.T, self.W[user].T))
            cb1 = np.sqrt(np.sum(np.multiply(np.dot(XVW,self.AInv[user]),XVW),axis=1))
            Theta_v_W = np.dot(self.Theta_v.T,self.W[user].T)
            var2 = [(np.dot(np.dot(Theta_v_W.T, self.CInv[item]),Theta_v_W)) for item in sampled_items]
            cb2 = np.sqrt(var2)
            ucb = score + self.alpha_u * cb1 + self.alpha_a * cb2

            selected_list = np.lexsort((tie_breaker, -ucb))[:self.config.list_size]
            rankings[i] = sampled_items[selected_list]

        return rankings

    def update(self, batch_users, rankings, clicks, round=None, user_round=None):
        for i in range(len(batch_users)):
            user = batch_users[i]

            # compute vec((X_a_t,V_a_t)W^T) -> list_size * (k+l)N
            XVW = self.create_vectorized_matrix(self.W.shape[0], self.W.shape[0] * (self.k + self.l), self.XV, self.W, range(len(rankings[i])))
            # XVW_optimal = self.create_vectorized_matrix(self.W.shape[0], self.W.shape[0] * (self.k + self.l), self.XV_optimal[sampled_items], self.W, rankings[i])

            _clicks, _ranking, _XVW = self.__collect_feedback(clicks[i], rankings[i], XVW)

            # discount_coef = [1 / (math.log(1 + j)) for j in range(1, len(rankings[0]) + 1)]
            # discount_coef_reward = [math.log(1 + j) for j in range(1, len(_clicks) + 1)]
            # discount_coef_penalization = [self.gamma * 1 / (math.log(1 + j)) for j in range(1, len(_clicks) + 1)]

            # if self.processing_type == 'recommended_discountfactor':
            #     self.exp_recommended[user][np.array(rankings[0])] += discount_coef
            # elif self.processing_type == 'examined_discountfactor':
            #     if len(clicks) == 0:
            #         self.exp_examined[user][np.array(rankings[0])] += discount_coef
            #     else:
            #         self.exp_examined[user][np.array(rankings[0][:len(clicks)])] += discount_coef[:len(clicks)]
            #
            # if self.processing_type == 'item_weight':
            #     _batch_features = self.update_item_weight(rankings[0], _batch_features, _clicks, discount_coef_penalization, discount_coef_reward, user, user_round)

            """
            This is for computing self.theta (Line 3-5 of Alogirthm 1 of NIPS 11)
            For fast matrix inverse, we use Woodbury matrix identity (https://en.wikipedia.org/wiki/Woodbury_matrix_identity)

            Return: self.theta is updated.
            """
            # for the inverse of M, feature matrix
            # XW * A^-1 * XW^T
            xAx = np.dot(_XVW, np.dot(self.AInv[user], _XVW.T))
            # (1/sigma I + xAx)^-1
            try:
                tmp_inv = np.linalg.inv(1 / self.sigma * np.eye(len(_XVW)) + xAx)
            except np.linalg.LinAlgError:
                # for the ill matrix. if the matrix is not invertible, we ignore this update
                self.ill_matrix_counter += 1
                return
            # A^-1*x^T
            AInv_xT = self.AInv[user].dot(_XVW.T)
            # AInv_xT*tmp_inv*AInv_xT^T
            self.AInv_tmp = np.dot(np.dot(AInv_xT, tmp_inv), AInv_xT.T)
            # MInv - the new part
            self.AInv[user] -= self.AInv_tmp
            # self.A[user] += self.sigma * _XVW.T.dot(_XVW)

            # for b: feedback
            # if self.processing_type == 'feature_weight':
            #     self.update_feature_weight(_batch_features, _clicks, discount_coef_penalization, discount_coef_reward,
            #                                user, user_round)
            # else:
            self.b[user] += np.dot(_clicks, _XVW)
            # for parameter Theta
            self.Theta = self.devectorize(np.dot(self.AInv[user], self.b[user]), self.k+self.l)
            # self.theta[self.theta < 0] = 0
            self.Theta_x = self.Theta[:, :self.k]
            self.Theta_v = self.Theta[:, self.k:]


            # ranking = rankings[i][:len(_clicks)]
            Theta_v_W = np.dot(self.Theta_v.T, self.W[user].T)
            xx = np.dot(Theta_v_W.reshape(self.Theta_v.shape[1],1), Theta_v_W.reshape(self.Theta_v.shape[1],1).T)
            for i in range(len(_ranking)):
                item = _ranking[i]
                self.C[item] += xx
                self.CInv[item] = np.linalg.inv(self.C[item])
                if self.contextual_var:
                    # print('a='+str(self.d.shape)+', b='+str(Theta_v_W.shape)+', c='+str(self.X[ranking].shape)+', d='+str(self.Theta_x.T.shape)+', e='+str(self.W[user])+', f='+str((_clicks[i] - np.dot(self.X[ranking],np.dot(self.Theta_x.T, self.W[user]))).shape))
                    # sys.stdout.flush()
                    # clicked_items_index = _clicks[i].nonzero()[0]
                    self.d[item] += Theta_v_W * (_clicks[i] - np.dot(self.X[item],np.dot(self.Theta_x.T, self.W[user])))
                else:
                    self.d[item] += Theta_v_W * _clicks[i]
                self.V[item] = np.dot(self.CInv[item], self.d[item])
            self.XV[:, self.k:] = self.V

            self.n_samples[user] += len(_clicks)
            self.n_clicks[user] += sum(_clicks)

    def __collect_feedback(self, click, ranking, batch_X):
        """
        :param y:
        :return: the last observed position.
        """
        # With  Cascade assumption, only the first click counts.
        if self.config.feedback_model == 'cascade':
            if np.sum(click) == 0:
                return click, ranking, batch_X
            first_click = np.where(click)[0][0]
            # batch_X[ranking[:first_click+1]] = np.zeros((ranking[:first_click+1][0], batch_X.shape[1]))
            return click[:first_click + 1], ranking[:first_click + 1], batch_X[:first_click + 1]
        elif self.config.feedback_model == 'dcm':
            if np.sum(click) == 0:
                return click, batch_X
            last_click = np.where(click)[0][-1]
            return click[:last_click + 1], ranking[:last_click + 1], batch_X[:last_click + 1]
        # all items are observed
        else:
            return click, ranking, batch_X

    def create_vectorized_matrix(self, n_rows, n_cols, first_matrix, second_matrix, selected_rows):
        mat = np.zeros((n_rows, n_cols))
        mat = [self.vectorize(np.dot(self.matrixize(second_matrix.shape[0], first_matrix.shape[1], first_matrix[row], row).T,second_matrix)) for row in selected_rows]
        return np.array(mat)

    def matrixize(self, n_rows, n_cols, vec, target_row):
        mat = np.zeros((n_rows, n_cols))
        mat[target_row] = vec
        return mat

    def vectorize(self, M):
        # temp = []
        # for i in range(M.shape[0]*M.shape[1]):
        # 	temp.append(M.T.item(i))
        # V = np.asarray(temp)
        # return V
        return np.reshape(M.T, M.shape[0] * M.shape[1])

    def devectorize(self, Vec, dimension):
        # temp = np.zeros(shape = (C_dimension, len(V)/C_dimension))
        # for i in range(len(V)/C_dimension):
        # 	temp.T[i] = V[i*C_dimension : (i+1)*C_dimension]
        # W = temp
        # return W
        # To-do: use numpy built-in function reshape.
        return np.reshape(Vec, (int(len(Vec) / dimension), dimension))