class StateStore {
  constructor(initialState = {}) {
    this.state = initialState
    this.listeners = []

    return new Proxy(this, {
      get: (target, prop) => {
        if (prop in target) {
          return target[prop]
        }
        return target.state[prop]
      },
      set: (target, prop, value) => {
        if (prop in target) {
          target[prop] = value
        } else {
          target.state[prop] = value
          target.notifyListeners()
        }
        return true
      }
    })
  }

  // Get the current state
  getState() {
    return {...this.state}
  }

  // Set the state directly
  setState(newState) {
    this.state = {...this.state, ...newState}
    this.notifyListeners()
  }

  // Update a specific property in the state
  updateState(key, value) {
    this.state[key] = value
    this.notifyListeners()
  }

  // Subscribe to state changes
  subscribe(listener) {
    this.listeners.push(listener)
    return () => {
      this.listeners = this.listeners.filter(l => l !== listener)
    }
  }

  // Notify all listeners about a state change
  notifyListeners() {
    this.listeners.forEach(listener => listener(this.getState()))
  }
}
