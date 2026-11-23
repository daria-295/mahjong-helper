An independent tool for analysing Riichi Mahjong hands, probabilities, and tile efficiency.

# Libraries I will use

- mss: *allows program to look at the Mahjong game without taking screenshots of entire desktop*
- opencv-python: *used to process screenshots, crop tiles, detect their positions, compare images and potentially recognise tiles.*
- numpy: *useful for representing tiles, manipulating image data, calculating probabilities and performing simulations.*
- PyTorch: *to train a neural network to recognise Mahjong tiles from screenshots*
- itertools, collections, random: *combinations, counting tiles, generating possible hands*
- PySide6: *the window displaying recommendations, probabilities, tile counts, and settings*

# Features to implement
- **Yaku & Hand Strategy Analysis**
  - Analyse potential Yaku and hand strategies
  - Calculate Shanten for each potential strategy
  - Calculate Ukeire and remaining useful tiles
  - Estimate the probability of completing different Yaku
  - Estimate potential hand value and completion time
  - Compare strategies based on tile efficiency and potential value

- **Hand Efficiency Analysis**
  - Calculate current Shanten
  - Analyse tile efficiency and hand flexibility
  - Identify useful tiles and possible improvements
  - Evaluate different hand configurations

- **Probability Calculator**
  - Calculate the probability of drawing specific tiles
  - Estimate the probability of reaching Tenpai within a given number of turns
  - Estimate the probability of completing a particular Yaku
  - Calculate the probability of completing a hand based on remaining tiles
  - Use simulations to estimate potential outcomes

- **AI Strategy Comparison**
  - Compare aggressive, defensive, tile-efficient and high-value strategies
  - Evaluate decisions based on hand progression, hand value, tile availability and score situation
  - Optimise strategy weights using simulated Mahjong scenarios
  - Compare AI performance against baseline strategies
 
- Trainer mode
  - Gives a random hand and asks the user what the best strategy is


# Checkpoints

## Phase 1
 - [x] Mahjong tile system
   - [x] Represent all 34 tile type
   - [x] Red Fives
    - [x] Tile combinations
    - [x] Prevent more than 4 copies of a tile
    

  - [x] Hand representation
    - [x] Create a Hand class
    - [x] Store concealed tiles
    - [x] Store tile counts efficiently
    - [x] Track red fives separately from normal fives
    - [x] Store existing melds
    - [x] Track whether the hand is open or close
  
  
  - [ ] Hand validation
    - [x] Validate tile inputs
    - [x] Check that no tile exceeds the maximum of four copies
    - [ ] Check whether the hand has the correct number of tiles
    - [ ] Account for existing melds when calculating hand size
    - [ ] Validate existing melds (correct tile combinations)
    - [x] Handle invalid hand configurations

  - [ ] Hand structure analysis
    - [ ] Identify pairs
    - [ ] Identify triplets
    - [ ] Identify sequences
    - [ ] Identify possible melds within concealed tiles
    - [ ] Identify incomplete sequences (e.g. 2m 3m)
    - [ ] Determine whether a hand is structurally complete
    - [ ] Recognise standard winning hand structure (4 melds + 1 pair)
    - [ ] Recognise special hand structures (e.g. Chiitoitsu and Kokushi)

  - [ ] Existing melds
    - [ ] Represent a meld as a data structure
    - [ ] Store the tiles belonging to each meld
    - [ ] Store whether a meld is open or closed
    - [ ] Support sequences (Chi)
    - [ ] Support triplets (Pon)
    - [ ] Support quads (Kan)
    - [ ] Distinguish between different types of Kan where relevant

## Phase 2
 - [ ] 1. Shanten calculator
 - [ ] 2. Tile availability and Ukiere
 - [ ] 3. Yaku detection
   - [ ] Common Yaku
   - [ ] Detecting combinations of Yaku
   - [ ] Account for open and closed hands
   

 - [ ] 4. Hand Scoring
   - [ ] Calculate Han
   - [ ] Calculate Fu
   - [ ] Calcualte final hand value
   - [ ] Account for dealer and non-dealer scoring

## Phase 3
 - [ ] 1. Hand efficiency analyser
   - [ ] Display current Shanten
   - [ ] Possible hand improvements
   - [ ] Evaluate hand flexibility

 - [ ] 2. Yaku and hand strategy analyser
   - [ ] Potential Yaku routes
   - [ ] Calculate Shanten for different Yaku routes
   - [ ] Compare Ukiere between routes
   - [ ] Estimate potential hand value
   - [ ] Compare efficiency against value
   - [ ] Recommend promising strategies

 - [ ] Probability calcualtor
   - [ ] Calculate probability of drawing a particular tile
   - [ ] Calculate probability of drawing useful tiles within N draws
    - [ ] Estimate probability of reaching Tenpai
    - [ ] Estimate probablity of completing a hand or Yaku
  

## Phase 4
   - [ ] Implement an efficiency-focused strategy
   - [ ] Implement an aggressive/high-value strategy
   - [ ] Implement a balanced strategy
   - [ ] Compare strategies across simulations
   - [ ] Experiment with optimising strategy weights
   - [ ] Evaluate performance against baseline strategies
  

## Phase 5
 - [ ] Create tile selector
 - [ ] Add hand editing and tile removal
 - [ ] Add seat selection
 - [ ] Display analysis results
 - [ ] Connect the GUI to analysis engine
 - [ ] Make entering a hand quick and intuitive (keyboard )



## Discontinued features
- discarding analyser
  - analyses each possible discard
    - e.g. Discard 1-Man: Resulting Shanten 1, useful tiles: 12, recommendation: poor(good/best)
  - calculates:
    - shanten before and after discarding
    - how flexible the resulting hand is
  - AI part:  Score = w1(tile efficiency) + w2(hand value) + w3(yaku probability) + w4(defence)
- Defensive play
  - enter which tiles the *opponents* have discarded, if opponent is in riichi/ has open hand, their seat position, enter the *specific opponent's* discard 
  - Risk vs Hand progression
    - e.g. Decision: discard 5-Man, hand progression: Fast, Risk: high, Expected value: medium
    - uses current shanten
    - consider estimated hand value
    - probability of reaching tenpai
    - probability of winning
    - risk of dealing into opponent

