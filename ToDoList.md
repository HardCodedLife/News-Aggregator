# A To Do List

## Tasks
Tasks need to be finished.

### Backend basic functionality
- [X] Config
- [X] Models
- [X] Services
- [X] API
- [X] Main
- [X] Migrate to LlamaIndex architecture

### Critical Issues
- [ ] **Reduce Docker dependencies to minimize disk usage**
  - Current: 146 packages including PyTorch + CUDA (~10GB+)
  - Goal: Strip to essential packages only
  - Issue: `llama-index-embeddings-huggingface` pulls in heavy torch dependencies

- [ ] **Fix Pydantic/Ollama compatibility issue**
  - Error: "1 validation error for ShowResponse model_info - Field required"
  - Attempted: Downgrade pydantic 2.12.5 → 2.11.5
  - Status: NOT YET SOLVED (blocked by disk space during Docker build)

- [ ] **Test backend to ensure robust operation**
  - Verify Ollama integration works
  - Test RAG pipeline end-to-end
  - Ensure streaming responses work correctly

### Frontend basic functionality
- [ ] My next move is here

### Improve Backend Later
- [ ] Chat improvements
- [ ] Error handling enhancement

---

## Ideas
- [ ] Provide a solid fact checking mechanism
- [ ] Consider lightweight embedding alternatives (avoid PyTorch if possible)
