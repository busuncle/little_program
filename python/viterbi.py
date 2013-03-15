# coding: utf8

"""
a demo for learning Hidden Markov Model(HMM) and Viterbi algorithm
"""

import random



states = ("s1", "s2")
observations = ("o1", "o2", "o3")
start_probabilities = {"s1": 0.6, "s2": 0.4}
transition_matrix = {
    "s1": {"s1": 0.7, "s2": 0.3},
    "s2": {"s1": 0.4, "s2": 0.6},
}
emission_matrix = {
    "s1": {"o1": 0.5, "o2": 0.4, "o3": 0.1},
    "s2": {"o1": 0.1, "o2": 0.3, "o3": 0.6},
}


def viterbi(obs, stat, start_p, trans_m, emit_m):
    # the two to-be-fill matrix, one contains probability, the other contains path node
    optimal_prob_m = [{}]
    optimal_path_m = [{}]

    # init start status
    for s in stat:
        optimal_prob_m[0][s] = start_p[s] * emit_m[s][obs[0]]
        optimal_path_m[0][s] = s

    # using dynamic programming method the fill the two matrix
    for t in xrange(1, len(obs)):
        optimal_prob_m.append({})
        optimal_path_m.append({})

        for s in stat:
            optimal_prob, optimal_stat = max([(optimal_prob_m[t - 1][si] * trans_m[si][s] * emit_m[s][obs[t]], si) for si in stat])
            optimal_prob_m[t][s] = optimal_prob
            optimal_path_m[t][s] = optimal_stat

    path = [max(optimal_prob_m[-1].iteritems(), key=lambda x:x[1])[0]]
    for i in xrange(len(obs) - 1, 0, -1):
        for s, ps in optimal_path_m[i].iteritems():
            if s == path[-1]:
                path.append(ps)
                break

    return path[::-1]



if __name__ == "__main__":
    res = viterbi(observations, states, start_probabilities, transition_matrix, emission_matrix)
    print res

