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

### Update 11/16

Good news: now VGGish embeddings are (num_frames, 128).

Bad news: results are still not ideal. 

Progress:
- Got embeddings for all frames
- Feature alignment has been completed
- Reimplemented similarity function

Embeddings used are postprocessed. Could switch back to pre-whitened embeddings to test. Similarities are obtained through dot product of 2 column vectors (one overall similarity score for each comparison). Might not be accurate due to feature alignment. Maybe for feature alignment, could do clip instead of duplication. 

-------------

Note: currently the embeddings extracted is ONLY the first block (around 1 second), so the result has a lot of room for improvement. 

