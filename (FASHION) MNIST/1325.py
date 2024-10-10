# MNIST手写数字分类（多种分类方法）
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

# 加载数据
mnist = load_digits()
data = mnist.data
print('data shape: ', mnist.data.shape)  # (1797,64)
print('target shape:', mnist.target.shape)  # (1797,)
print('image shape:', mnist.images.shape)  # (1797,8,8)

# 分割数据，将25%的数据作为测试集，其余作为训练集
train_x, test_x, train_y, test_y = train_test_split(data, mnist.target, test_size=0.25, random_state=33)

# 创建LR分类器
model = LogisticRegression()
model.fit(train_x, train_y)
predict_y=model.predict(test_x)
print('LR准确率: %0.4lf' % accuracy_score(predict_y, test_y))

# 创建GaussianNB分类器
model = GaussianNB()
model.fit(train_x, train_y)
predict_y=model.predict(test_x)
print('GaussianNB准确率: %0.4lf' % accuracy_score(predict_y, test_y))

# 创建MultinomialNB分类器
model = MultinomialNB()
model.fit(train_x, train_y)
predict_y=model.predict(test_x)
print('MultinomialNB准确率: %0.4lf' % accuracy_score(predict_y, test_y))

# 创建BernoulliNB分类器
model = BernoulliNB()
model.fit(train_x, train_y)
predict_y=model.predict(test_x)
print('BernoulliNB准确率: %0.4lf' % accuracy_score(predict_y, test_y))

# 创建决策树分类器
model = DecisionTreeClassifier()
model.fit(train_x, train_y)
predict_y=model.predict(test_x)
print('决策树准确率: %0.4lf' % accuracy_score(predict_y, test_y))

# 创建随机森林分类器
model = RandomForestClassifier()
model.fit(train_x, train_y)
predict_y=model.predict(test_x)
print('随机森林准确率: %0.4lf' % accuracy_score(predict_y, test_y))

# 创建SVM分类器
model = SVC()
model.fit(train_x, train_y)
predict_y=model.predict(test_x)
print('SVC准确率: %0.4lf' % accuracy_score(predict_y, test_y))
