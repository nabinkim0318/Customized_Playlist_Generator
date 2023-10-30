To get the cosine similarity of input files, cd into cosSimVGGish and run ```python3 main.py```

To upload big files that exceed 100MB, install git-lfs with brew: ```brew install git-lfs``` (Mac)

Then do:
```
git lfs install
git lfs track "*.ckpt" # file extension of the file that exceeds file size limit
git add .
git commit -m "commit-message"
git push
```


Note: currently the embeddings extracted is ONLY the first block (around 1 second), so the result has a lot of room for improvement. 