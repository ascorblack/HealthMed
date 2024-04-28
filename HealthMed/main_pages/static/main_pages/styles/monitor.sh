inotifywait -e close_write,moved_to,create -m . |
while read -r directory events filename; do
  if [ "$filename" = "header.scss" ]; then
    echo $(date) "header.scss --> header.css"
    sass header.scss header.css
    echo $(date) "completed"
  fi
  if [ "$filename" = "index.scss" ]; then
    echo $(date) "index.scss --> index.css"
    sass index.scss index.css
    echo $(date) "completed"
  fi
  if [ "$filename" = "footer.scss" ]; then
    echo $(date) "footer.scss --> footer.css"
    sass footer.scss footer.css
    echo $(date) "completed"
  fi
  if [ "$filename" = "forms.scss" ]; then
    echo $(date) "forms.scss --> forms.css"
    sass forms.scss forms.css
    echo $(date) "completed"
  fi
done
