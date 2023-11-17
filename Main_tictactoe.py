from TD_lambda import TD_lambda
from MonteCarlo import MonteCarlo
from TD_Zero import TD_zero
from vs_human import vs_human_game

if __name__ == "__main__":

    print("Choose an option:")
    print("1. Play against Monte Carlo agent")
    print("2. Play against TD Zero agent")
    print("3. Play against TD lambda agent")

    choice = input("Enter your choice (1, 2, or 3): ")
    
    agent = None
    if choice == "1":
        agent = MonteCarlo()
       
    elif choice == "2":
        agent = TD_zero()
      
    elif choice == "3":
        agent = TD_lambda()

    if agent is not None :
        agent.train(10000)
        vs_human_game(agent)
    else:
         print("Invalid choice. Please enter 1, 2, or 3.")

    
