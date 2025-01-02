document.getElementById('box-dimensions-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const length = document.getElementById('length').value;
    const breadth = document.getElementById('breadth').value;
    const height = document.getElementById('height').value;

    fetch('/generate-box-layout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ length, breadth, height })
    })
    .then(response => response.blob())
    .then(blob => {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'box_layout.svg';
        link.click();
    });
});
