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

### Update 12/6
* MFCCs work better than all baseline features
* VGGish is (num_windows, 128), baseline features is (num_windows, num_features). The num_windows don't exactly align yet. Need to either clip or align. 
* [dim-sim](https://jongpillee.github.io/multi-dim-music-sim/) evaluation dataset. 


### Update 12/5

TOFIX:
- For some reason, similarity does not have matching dimensions for baseline features. 
- Spectral crest only has 1 value for the entire audio, need to check why (currently just have it repeated the number of blocks times)
- Baseline feature currently has dimension of (19, num_blocks) 6 + 13 MFCCs
- If we are keeping all embedding blocks and all baseline feature blocks, then we need to match the window and block size of the two. 
- Could potentially also have a summary statistics of all features instead of block by block.
- Moved global config variables to config.py

### Update 11/23
* Alternative feature alignment (clipping) created, does not work as well as repetitive feature alignment. 
    - Makes sense, since it gives us more information. 
* Post processing causes loss of information, and hence result in a worse performing similarity function. 
    > The released AudioSet embeddings were postprocessed before release by applying a PCA transformation (which performs both PCA and whitening) as well as quantization to 8 bits per embedding element. This was done to be compatible with the YouTube-8M project which has released visual and audio embeddings for millions of YouTube videos in the same PCA/whitened/quantized format.

    - both dimensionality reduction and quantization will cause loss of information. 

### Update 11/21
* MSD subset:
    - the start points seem to be kind of random
* Moved the location of VGGish model creation
* Swapped to embeddings before whitening and before quantization:
    - Results significantly improved compared to the times before
    - Human listening test: seems like pre-whitening and pre-quantization performs better
    - Range of similarities: pre-whitening and pre-quanitzation has a bigger range and result is closer to perception
* Yet to implement alternative feature alignment but placeholder implemented




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

