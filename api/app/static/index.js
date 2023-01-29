function deleteFile(fileId) {
    fetch("/files/delete-file", {
      method: "POST",
      body: JSON.stringify({ fileId: fileId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }

