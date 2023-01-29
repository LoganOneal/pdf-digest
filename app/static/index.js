function deleteFile(fileId) {
    fetch("/files/delete", {
      method: "POST",
      body: JSON.stringify({ fileId: fileId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

  function downloadFile(fileId) {
    fetch("/files/download", {
      method: "POST",
      body: JSON.stringify({ fileId: fileId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

