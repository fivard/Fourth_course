module Main where

import GHC.Conc
import System.IO

numbersAtOddPosition :: [a] -> [a]
numbersAtOddPosition [] = []
numbersAtOddPosition [x] = []
numbersAtOddPosition (x:y:xs) = y : numbersAtOddPosition xs

numbersAtEvenPosition :: [a] -> [a]
numbersAtEvenPosition [] = []
numbersAtEvenPosition [x] = [x]
numbersAtEvenPosition (x:y:xs) = x : numbersAtEvenPosition xs

merge :: Ord a => [a] -> [a] -> [a]
merge [] [] = []
merge [] y = y
merge x [] = x
merge (x:xs) (y:ys)
    | x <= y = x : merge xs (y:ys)
    |otherwise =  y : merge (x:xs) ys

batchersMerge :: Ord a => [a] -> [a]
batchersMerge [] = []
batchersMerge [x] = [x]
batchersMerge arr
    | length (arr) > 2 = merge mergedEvens mergedOdds
    | otherwise = merge [head arr] [last arr]
    where
        mergedEvens = batchersMerge (numbersAtEvenPosition arr)
        mergedOdds = batchersMerge (numbersAtOddPosition arr)

batchersSort :: Ord a => [a] -> [a]
batchersSort [] = []
batchersSort [x] = [x]
batchersSort arr = leftSorted `par` rightSorted `pseq` batchersMerge $ leftSorted ++ rightSorted
    where
        (left,right) = splitList arr
        leftSorted = batchersSort left
        rightSorted = batchersSort right

splitList :: [a] -> ([a], [a])
splitList [] = ([],[])
splitList [x] = ([x],[])
splitList xs = splitAt mid xs
        where mid = (length xs) `div` 2

stoi :: [String] -> [Int]
stoi = map read

main = do
        let listToSort = []
        handle <- openFile "data.txt" ReadMode
        contents <- hGetContents handle
        let singlewords = words contents
            listToSort = stoi singlewords
        print listToSort
        hClose handle
        print(batchersSort listToSort)