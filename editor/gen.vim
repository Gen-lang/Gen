" Vim syntax file
" Language: Gen

if exists("b:current_syntax")
    finish
endif

" Language keywords
syntax keyword genKeywords var

" Type keywords
syntax keyword genType INT FLOAT

" Numbers
syntax match genNumbers "\d\+"

" Set highlights
highlight default link genKeywords Repeat
highlight default link genNumbers Number
highlight default link genType Type

let b:current_syntax = "gen"