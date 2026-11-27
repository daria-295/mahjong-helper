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

## 1. Core Mahjong system
- [x] Mahjong tile system (34 tiles, Red Fives)
- [x] Hand representation and tile management
- [x] Meld representation (Chi, Pon, Kan)
- [x] Meld combination validation
- [x] Hand structure analysis and decomposition
- [ ] Complete hand validation
- [ ] Distinguish different Kan types
- [ ] Identify all possible concealed melds

## 2. Mahjong analysis engine
### Shanten calculator
- [x] Standard Shanten calculation
- [x] Recursive hand grouping
- [x] Complete hand, Tenpai and one-Shanten tests
- [ ] Test existing melds and edge cases
- [x] Chiitoitsu Shanten
- [x] Kokushi Musou Shanten
- [x] Calculate minimum Shanten across all hand types

### Tile availability and Ukeire
- [x] Identify improving tiles
- [x] Calculate remaining tile copies
- [x] Calculate total Ukeire
- [x] Identify winning waits
- [x] Account for visible tiles

### Yaku detection
- [x] All listed regular Yaku
- [x] All 12 base Yakuman
- [x] Open/closed hand considerations
- [x] Ron/Tsumo and situational conditions
- [ ] Full edge-case verification and double Yakuman variants

### Hand scoring
- [ ] Calculate Han and Fu
- [ ] Calculate Dora, Ura Dora, Aka Dora and Kan Dora
- [ ] Calculate final hand value
- [ ] Dealer/non-dealer scoring
- [ ] Mangan, Haneman, Baiman, Sanbaiman and Yakuman

## 3. Hand analysis and probability
### Hand efficiency analyser
- [ ] Calculate current Shanten
- [ ] Identify useful tiles and improvements
- [ ] Evaluate hand flexibility
- [ ] Compare possible discards
- [ ] Recommend best discards

### Yaku and hand strategy analyser
- [ ] Identify potential Yaku routes
- [ ] Calculate Shanten for different strategies
- [ ] Compare Ukeire between strategies
- [ ] Estimate potential hand value
- [ ] Balance efficiency against value
- [ ] Recommend promising strategies

### Probability calculator
- [ ] Calculate tile drawing probabilities
- [ ] Estimate useful draws within N turns
- [ ] Estimate probability of reaching Tenpai
- [ ] Estimate probability of completing a hand or Yaku
- [ ] Simulate possible outcomes

## 4. AI strategy and training
- [ ] Implement efficiency-focused strategy
- [ ] Implement aggressive/high-value strategy
- [ ] Implement defensive strategy
- [ ] Implement balanced strategy
- [ ] Build Mahjong game simulator
- [ ] Compare strategies across simulations
- [ ] Optimise strategy weights
- [ ] Train AI using PyTorch
- [ ] Evaluate AI against baseline strategies

## 5. Computer vision and game recognition
- [ ] Capture game using mss
- [ ] Process screenshots using OpenCV
- [ ] Detect and crop individual tiles
- [ ] Create tile image dataset
- [ ] Train PyTorch tile recognition model
- [ ] Recognise all 34 tiles and Red Fives
- [ ] Detect opponent discards and melds
- [ ] Track visible tiles during a game

## 6. PySide6 GUI
- [ ] Create desktop application
- [ ] Create tile selector
- [ ] Add hand editing and tile removal
- [ ] Add seat and round selection
- [ ] Display analysis results
- [ ] Display recommended discards and probabilities
- [ ] Connect GUI to analysis engine
- [ ] Make hand entry quick and intuitive (keyboard support)
- [ ] Integrate live game recognition

## 7. Trainer mode
- [ ] Generate random Mahjong hands
- [ ] Ask user to choose the best discard or strategy
- [ ] Evaluate the user's decision
- [ ] Explain the recommended move
- [ ] Track accuracy and progress
- [ ] Add difficulty levels



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

