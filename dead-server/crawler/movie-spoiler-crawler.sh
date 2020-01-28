#! /bin/sh
content=$(curl -L themoviespoiler.com)
echo $content
for string in "$(echo $content | grep -e "<body")"
do
    match="${match:+$match }$string"
    # echo $matchs
done

# string="string to search 99 with 88 some 42 numbers"
pattern="(http:\/\/themoviespoiler.com\/movies\/.*[a-zA-z]+\/)"

for word in $content
do
    [[ $word =~ $pattern ]]
    if [[ ${BASH_REMATCH[0]} ]]
    then
        match="${match:+match }${BASH_REMATCH[0]}"
        echo $match
    fi
done

# for string in "$(echo $result | grep -e "(http:\/\/themoviespoiler.com\/movies\/.*[a-zA-z]+\/)")"
# do
#     match="${match:+$match }$string"
#     echo $match
# done

# content2=grep '(http:\/\/themoviespoiler.com\/movies\/.*[a-zA-z]+\/)' <<<$content
# echo $content2
