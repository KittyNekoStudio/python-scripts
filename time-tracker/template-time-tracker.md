" The day is in a heading in the format Year-Month-Day
" In the body of a heading there are different activities followed by a 
" time in Hour:Minute:Second format
" The parser reads each day as a seperate dictionary wich gets put inside a main dictionary
" creating a 2D dictionary
" The key of the day dictionary are the activity names and the value is the time stored as a tuple
" It would look like this
" {"2025-1-20": {"Japanese": (2, 32, 1)}, "2025-1-21": {"Japanese": (0, 3, 28), "Coding": (3, 12, 18)}}

" Basic Outline
" ## Day 0

" Comment
" - Tag: Time

## 2025-1-20

- Japanese-1: 2:32:1

## 2025-1-21

- Japanese-1: 0:3:28
- Coding-1: 3:12:18
