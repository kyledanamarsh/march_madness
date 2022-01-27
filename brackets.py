class Participants:

    def __init__(self, name):
        self.name = name
        #points is for the column and cell of the points for this particular
        #participant.
        self.points = ''
        self.score = 0
        self.addition = 0
        self.number = '' #This is their phone number
        self.round = ''
        pass


Results = Participants("Results")

# Create participants (whoever is playing in your bracket) in this file by
# assigning them variables as shown below:
# 
# Participant_A = Participants(participant_name)
#
# Then assign them values like this:
#
# Participant_A.number = '1234567890'
# Participant_A.points = 'Points!A1'