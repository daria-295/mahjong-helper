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
   - [x] Represent all 34 tile types
   - [x] Represent Red Fives separately
    - [x] Define tile combinations and suit ordering
    - [x] Prevent more than 4 copies of a tile
    

  - [x] Hand representation
    - [x] Create a Hand class
    - [x] Store concealed tiles
    - [x] Store tile counts efficiently
    - [x] Track red fives separately from normal fives
    - [x] Store existing melds
    - [x] Track whether the hand is open or closed
    - [x] Add and remoe tiles
    - [x] Count total tiles and individual tile tpes
    - [x] Clear a hand
  
  
  - [ ] Hand validation
    - [x] Check whether the hand has the correct number of tiles
    - [x] Account for existing melds when calculating hand size
    - [x] Validate tile inputs
    - [ ] Check that no tile exceeds the maximum of four copies
    - [x] Validate existing melds (correct tile combinations)
    - [x] Handle invalid inputs and basic invalid configurations

  - [ ] Existing melds
    - [x] Represent a meld as a data structure
    - [x] Store the tiles belonging to each meld
    - [x] Store whether a meld is open or closed
    - [x] Support sequences (Chi)
    - [x] Support triplets (Pon)
    - [x] Support quads (Kan)
    - [x] Validate legal Chi combinations
    - [x] Validate legal Pon combinations
    - [x] Validate legal Kan combinations
    - [ ] Distinguish between different types of Kan where relevant


  - [ ] Hand structure analysis
    - [x] Identify pairs
    - [x] Identify triplets
    - [x] Identify sequences
    - [x] Identify adjacent incomplete sequences (e.g. 2m 3m)
    - [x] Identify gapped incomplete sequences (e.g. 2m 4m)
    - [x] Determine whether a hand is structurally complete
    - [x] Recognise standard winning hand structure (4 melds + 1 pair)
    - [x] Recognise Seven Pairs
    - [x] Recognise Thirteen Orphans
    - [x] Return possible standard-hand decompositions
    - [ ] dentify and return all possible melds within concealed tiles independently


## Phase 2
 - [ ] 1. Shanten calculator
    - [x] Find first remaining tile
    - [x] Recursively explore possible groupings
    - [x] Identify complete melds
    - [x] Identify pairs
    - [x] Identify incomplete melds (taatsu)
    - [x] Calculate standard-hand shanten
    - [x] Account for existing melds in the formula
    - [x] Test complete hands (-1)
    - [x] Test Tenpai hands (0)
    - [x] Test one-shanten hands (1)
    - [x] Test multiple pairs and alternative groupings
    - [ ] Test hands containing existing melds
    - [ ] Test edge cases and unusual groupings
    - [ ] Implement Chiitoitsu shanten
    - [ ] Implement Kokushi Musou shanten
    - [ ] Return the minimum shanten across all applicable hand types


  - [ ] 2. Tile availability and Ukeire
    - [ ] Identify tiles that improve the hand
    - [ ] Calculate remaining copies of each tile
    - [ ] Calculate total Ukeire
    - [ ] Identify winning tiles (waits)
    - [ ] Account for visible tiles and existing melds


  - [x] 3. Yaku detection
  - [x] Regular Yaku
    - [x] Riichi
    - [x] Double Riichi
    - [x] Ippatsu
    - [x] Menzen Tsumo
    - [x] Tanyao
    - [x] Yakuhai
    - [x] Pinfu
    - [x] Iipeikou
    - [x] Ryanpeikou
    - [x] Toitoi
    - [x] Honitsu
    - [x] Chinitsu
    - [x] Chanta
    - [x] Junchan
    - [x] Sanshoku Doujun
    - [x] Sanshoku Doukou
    - [x] Ittsu
    - [x] Honroutou
    - [x] Shousangen
    - [x] Sanankou
    - [x] Sankantsu
    - [x] Chiitoitsu
    - [x] Rinshan Kaihou
    - [x] Chankan
    - [x] Haitei
    - [x] Houtei
  - [ ] Yakuman
    - [x] Daisangen
    - [x] Shousuushi
    - [x] Daisuushi
    - [x] Suuankou
    - [x] Suukantsu
    - [x] Tsuuiisou
    - [x] Chinroutou
    - [x] Ryuuiisou
    - [x] Chuuren Poutou
    - [x] Kokushi Musou
    - [x] Tenhou
    - [x] Chiihou
  

- [ ] 4. Hand scoring
    - [ ] Calculate Han
    - [ ] Calculate Fu
    - [ ] Calculate final hand value
    - [ ] Account for dealer and non-dealer scoring
    - [ ] Account for limit hands (Mangan, Haneman, Baiman, Sanbaiman, Yakuman)
    - [ ] Account for Dora, Ura Dora, Aka Dora and Kan Dora
## Phase 3
 - [ ] 1. Hand efficiency analyser
   - [ ] Display current Shanten
   - [ ] Display possible hand improvments
   - [ ] Evaluate hand flexibility
   - [ ] Recommend tiles to discard

 - [ ] 2. Yaku and hand strategy analyser
   - [ ] Identify potential Yaku routes
   - [ ] Calculate Shanten for different Yaku routes
   - [ ] Compare Ukiere between routes
   - [ ] Estimate potential hand value
   - [ ] Compare efficiency against value
   - [ ] Recommend promising strategies

 - [ ] 3. Probability calcualtor
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

