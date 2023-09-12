brew install chromedriver --cask &&
cd '/opt/homebrew/bin/' &&                      # Scarica chromedriver
xattr -d com.apple.quarantine chromedriver &&   # Permette esecuzione chromedriver

brew install google-chrome --cask               # Installa Google Chrome