const touchHandler = (event: any) => {
    if (event.touches.length > 1) {
      event.preventDefault();
    }
  };
  document.addEventListener('touchstart', touchHandler, {
    passive: false
  });