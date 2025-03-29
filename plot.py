import matplotlib.pyplot as plt

def plot_progress(best_scores):
    plt.figure()
    plt.plot(best_scores, marker='o')
    plt.title("Progress of Genetic Algorithm")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
