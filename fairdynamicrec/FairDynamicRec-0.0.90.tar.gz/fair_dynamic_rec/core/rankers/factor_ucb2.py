import numpy as np
from .abstract_ranker import AbstractRanker

# Objective function: min 1/2 (X - U . V_T) + 1/2 * \lambda (U)^2 + 1/2 * \lambda (V)^2

class FactorUCB1(AbstractRanker):
    def __init__(self, config, dataObj, parameters=None):
        super(FactorUCB1, self).__init__(config, dataObj)
        self.prng = np.random.RandomState(seed=config.seed)
        self.k = 0
        self.contextual_var = bool(parameters["contextual_variable"]["value"]) if "contextual_variable" in parameters else False
        if self.contextual_var:
            self.X = self.dataObj.feature_data['train_item_topical_features']
            self.k = self.X.shape[1]
        self.l = int(parameters["latent_dim"]["value"]) if "latent_dim" in parameters else 0
        self.lambda_1 = float(parameters["lambda1"]["value"]) if "lambda1" in parameters else 1.0
        self.lambda_2 = float(parameters["labmda2"]["value"]) if "lambda2" in parameters else 1.0
        self.alpha_a = float(parameters["alpha_a"]["value"]) if "alpha_a" in parameters else 1.0
        self.alpha_u = float(parameters["alpha_u"]["value"]) if "alpha_u" in parameters else 1.0

        self.batch_features = None

        self.U = np.zeros((self.dataObj.n_users, self.k+self.l))
        self.V = np.zeros((self.dataObj.n_items, self.l))

        self.W = np.ones((self.dataObj.n_users, self.dataObj.n_users))

        self.A = self.lambda_1 * np.identity(n=self.k+self.l)
        self.AInv = np.linalg.inv(self.A) #np.zeros((self.k+self.l,self.k+self.l))
        self.b = np.zeros((self.dataObj.n_users,self.k+self.l))

        self.C = self.lambda_2 * np.identity(n=self.l)
        self.CInv = np.linalg.inv(self.C)
        self.d = np.zeros((self.dataObj.n_users, self.l))


    def get_ranking(self, batch_users, sampled_items=None, round=None):
        rankings = np.zeros((len(batch_users), self.config.list_size), dtype=int)
        self.batch_features = np.zeros((len(batch_users), self.config.list_size, self.k+self.l))
        if self.contextual_var:
            items_feature = np.concatenate((self.X, self.V), axis=1)
            user_topic = self.U[:,:self.k]
            user_latent = self.U[:, self.k:]
        else:
            items_feature = self.V
            user_latent = self.U
        tie_breaker = self.prng.rand(len(sampled_items))
        for i in range(len(batch_users)):
            user = batch_users[i]

            XVW = np.dot(items_feature[sampled_items].T,self.W)
            cb1 = self.alpha_u * np.sqrt(np.multiply(np.dot(XVW.T,self.AInv),XVW.T))
            cb2 = self.alpha_a * np.sqrt(np.dot(np.dot(np.dot(user_latent.T, self.W).T, self.CInv), np.dot(user_latent.T, self.W[user]).T))
            score = np.dot(items_feature[sampled_items], np.dot(self.U.T, self.W[user]))
            ucb = score + cb1.T + cb2.T

            rankings[i] = np.lexsort((tie_breaker, -ucb))[:self.config.list_size]
            # if self.contextual_var:
            #     self.batch_features[i] = np.concatenate((self.X[rankings[i]], self.dataObj.feature_data['test_item_latent_features'][rankings[i]]), axis=1)
            # else:
            #     self.batch_features[i] = self.dataObj.feature_data['test_item_latent_features'][rankings[i]]
        return rankings

    def update(self, batch_users, sampled_items, rankings, clicks, round=None, user_round=None):
        for i in range(len(batch_users)):
            user = batch_users[i]

            X = np.zeros((self.V.shape[0], self.k + self.l))
            if self.contextual_var:
                X[rankings[i]] = np.concatenate((self.X[rankings[i]], self.dataObj.feature_data['test_item_latent_features'][rankings[i]]), axis=1)
            else:
                X[rankings[i]] = self.dataObj.feature_data['test_item_latent_features'][rankings[i]]
            X = X[sampled_items]

            _clicks, _X = self.__collect_feedback(clicks, i, rankings, X)

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

            cb1 = self.alpha_u * np.sqrt(np.dot(np.dot(np.dot(items_feature[sampled_items].T, self.W[user].T).T, self.AInv), np.dot(items_feature[sampled_items].T, self.W.T)))
            cb2 = self.alpha_a * np.sqrt(np.dot(np.dot(np.dot(user_latent.T, self.W[user]).T, self.CInv), np.dot(user_latent.T, self.W[user])))
            """
            This is for computing self.theta (Line 3-5 of Alogirthm 1 of NIPS 11)
            For fast matrix inverse, we use Woodbury matrix identity (https://en.wikipedia.org/wiki/Woodbury_matrix_identity)

            Return: self.theta is updated.
            """
            # (X,V) * W
            XVW = np.dot(X.T, self.W).T
            # for the inverse of M, feature matrix
            # XW * A^-1 * x^T
            xAx = np.dot(XVW, np.dot(self.AInv, XVW.T))
            # (1/sigma I + xAx)^-1
            try:
                tmp_inv = np.linalg.inv(1 / self.sigma * np.eye(len(XVW)) + xAx)
            except np.linalg.LinAlgError:
                # for the ill matrix. if the matrix is not invertible, we ignore this update
                self.ill_matrix_counter += 1
                return
            # A^-1*x^T
            AInv_xT = self.AInv.dot(XVW.T)
            # AInv_xT*tmp_inv*AInv_xT^T
            self.AInv_tmp = np.dot(np.dot(AInv_xT, tmp_inv), AInv_xT.T)
            # MInv - the new part
            self.AInv -= self.AInv_tmp

            self.A += self.sigma * XVW.T.dot(XVW)

            # for b: feedback
            # if self.processing_type == 'feature_weight':
            #     self.update_feature_weight(_batch_features, _clicks, discount_coef_penalization, discount_coef_reward,
            #                                user, user_round)
            # else:
            self.b += np.dot(_clicks, XVW)

            # self.b_tmp[user] = np.dot(_clicks, _batch_features)
            # self.b[user] += self.b_tmp[user]

            # for parameter theta
            self.theta[user] = np.dot(self.MInv[user], self.b[user])
            # self.theta[self.theta < 0] = 0

            self.n_samples[user] += len(_clicks)
            self.n_clicks[user] += sum(_clicks)

    def __collect_feedback(self, clicks, batch_user_id, rankings, batch_X):
        """
        :param y:
        :return: the last observed position.
        """
        # With  Cascade assumption, only the first click counts.
        if self.config.feedback_model == 'cascade':
            if np.sum(clicks[batch_user_id]) == 0:
                return clicks[batch_user_id], batch_X
            first_click = np.where(clicks[batch_user_id])[0][0]
            batch_X[rankings[:first_click+1]] = np.zeros((rankings[:first_click+1], batch_X.shape[1]))
            return clicks[batch_user_id][:first_click + 1], self.batch_features[batch_user_id][:first_click + 1]
        elif self.config.feedback_model == 'dcm':
            if np.sum(clicks[batch_user_id]) == 0:
                return clicks[batch_user_id], self.batch_features[batch_user_id]
            last_click = np.where(clicks[batch_user_id])[0][-1]
            return clicks[batch_user_id][:last_click + 1], self.batch_features[batch_user_id][:last_click + 1]
        # all items are observed
        else:
            return clicks[batch_user_id], self.batch_features[batch_user_id]

    def vectorize(self, M):
        # temp = []
        # for i in range(M.shape[0]*M.shape[1]):
        # 	temp.append(M.T.item(i))
        # V = np.asarray(temp)
        # return V
        return np.reshape(M.T, M.shape[0] * M.shape[1])