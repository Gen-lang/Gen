" Vim syntax file
" Language: Gen

" Usage Instructions
" Put this file to ~/.vim/syntax directory:
"	(if you are on Mac) cp editor/gen.vim ~/.vim/syntax/
" And add the following line to your ~/.vimrc: 
" autocmd BufRead,BufNewFile *.gen set filetype=gen

if exists("b:current_syntax")
    finish
endif

" Language keywords
syntax keyword genKeywords var and or not if elseif else for through step while then

" Type keywords
syntax keyword genType int float nothing

" Boolean
syntax keyword genBool true false

" Numbers
syntax match genNumbers "\d\+"

" Set highlights
highlight default link genKeywords Repeat
highlight default link genNumbers Number
highlight default link genType Type
highlight default link genBool Boolean

let b:current_syntax = "gen"