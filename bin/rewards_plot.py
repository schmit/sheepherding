import matplotlib.pyplot as plt
import seaborn as sns
import pickle

from sheepherding.util import runningAvg

f, ax = plt.subplots(1, 1, figsize=(8,6))


filenames = [('linear: 0.05','rewards_linear_05.pkl'), ('linear 0.25','rewards_linear_25.pkl'), ('linear adaptive', 'rewards_linear.pkl'), ('baseline', 'rewards_baseline.pkl')]
for model, fn in filenames:
    with open(fn, 'r') as fl:
        rewards = pickle.load(fl)

    ax.plot(range(1, len(rewards)+1), runningAvg(rewards), '-', label=model)

ax.legend(loc=4)
ax.set_xlim(0, len(rewards))

ax.set_title('Convergence of Q-learning')
ax.set_xlabel('Run')
ax.set_ylabel('Running average of rewards')


f.tight_layout()
f.savefig('rewards.jpg')

