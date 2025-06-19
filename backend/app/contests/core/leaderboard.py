class leaderboard_entry:
    def __init__(self, leaderboard, user_id, username):
        self.user_id = user_id
        self.username = username
        self.leaderboard = leaderboard
        self.problem_legend = leaderboard.problem_legend
        self.problem_count = len(self.problem_legend)

        self.times = [0] * self.problem_count 
        self.attempts = [0] * self.problem_count 
        self.solved = [False] * self.problem_count 

        self.solves = 0;
    
    def set_submission(self, problem_letter, time, accepted):
        index = self.problem_legend[problem_letter]
        self.times[index] = max(self.times[index], time)
        self.attempts[index] += 1
        self.solved[index] = self.solved[index] or accepted
        if accepted:
            self.solves += 1

    # ICPC score
    # Score: sum of times + 20 * attempts for each solved problem
    def get_score(self):
        score = 0
        for i, solved in enumerate(self.solved):
            if solved:
                score += self.times[i] + self.attempts[i] * 20
        return score
    # TODO handle resubmission
    # ICPC ordering
    # Comparison rules: First by solve #, then by score, then by slowest solves, finally undefined
    def __lt__(self, other):
        if self.solves != other.solves:
            return self.solves > other.solves
        if self.get_score() != other.get_score():
            return self.get_score() < other.get_score()
        
        tiebreak_self = sorted(self.times, reverse=True)
        tiebreak_other = sorted(other.times, reverse=True)
        for i in range(self.problem_count):
            if tiebreak_self[i] != tiebreak_other[i]:
                return tiebreak_self[i] < tiebreak_other[i]
            
        return self.user_id < other.user_id  # Literally impossible lmao
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "solves": self.solves,
            "score": self.get_score(),
            "times": self.times,
            "attempts": self.attempts,
            "solved": self.solved
        }

class leaderboard:
    def __init__(self, users, problem_legend):
        self.users = users
        self.problem_legend = problem_legend
        self.entries = {user_id: leaderboard_entry(self, user_id, users[user_id]) for user_id in users}
    
    def set_submission(self, user_id, problem_letter, time, accepted):
        if user_id not in self.entries:
            return
        
        self.entries[user_id].set_submission(problem_letter, time, accepted)
    
    def get_sorted_entries(self):
        return sorted(self.entries.values())
    
    def to_dict(self):
        return {
            "problem_legend": self.problem_legend,
            "entries": [entry.to_dict() for entry in self.get_sorted_entries()]
        }
    

