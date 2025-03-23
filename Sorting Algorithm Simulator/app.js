// Referências dos elementos do DOM
const startButton = document.getElementById('start-button');
const resetButton = document.getElementById('reset-button');
const algorithmSelect = document.getElementById('algorithm-select');
const arraySizeInput = document.getElementById('array-size');
const speedInput = document.getElementById('speed');
const arraySizeValue = document.getElementById('array-size-value');
const speedValue = document.getElementById('speed-value');
const visualizationContainer = document.getElementById('visualization-container');
const statusText = document.getElementById('status');

// Elementos de música
const backgroundMusic = document.getElementById('background-music');
const playMusicButton = document.getElementById('play-music');
const pauseMusicButton = document.getElementById('pause-music');
const volumeControl = document.getElementById('volume');
const musicSelect = document.getElementById('music-select');

// Elementos do YouTube
const youtubeToggle = document.getElementById('youtube-toggle');
const youtubeControls = document.getElementById('youtube-controls');
const youtubeUrl = document.getElementById('youtube-url');
const loadYoutubeButton = document.getElementById('load-youtube');
const youtubePlayerContainer = document.getElementById('youtube-player-container');
const normalAudioPlayer = document.getElementById('normal-audio-player');

// Variáveis para o YouTube
let youtubePlayer = null;

// Variáveis de controle
let array = [];
let isSorting = false;
let delay = 200;  // Atraso por padrão

// Atualiza os valores do tamanho do vetor e a velocidade da animação
arraySizeInput.addEventListener('input', () => {
  arraySizeValue.textContent = arraySizeInput.value;
  resetArray();
});

speedInput.addEventListener('input', () => {
  delay = speedInput.value;
  speedValue.textContent = `${delay}ms`;
});

// Botão de reinício
resetButton.addEventListener('click', resetArray);

// Gera um novo vetor aleatório
function resetArray() {
  if (isSorting) return; // Não resetar durante a ordenação
  
  const size = parseInt(arraySizeInput.value);
  array = generateArray(size);
  renderArray(array);
  statusText.textContent = '';
  startButton.disabled = false;
}

// Gera um vetor aleatório de números
function generateArray(size) {
  let arr = [];
  for (let i = 0; i < size; i++) {
    arr.push(Math.floor(Math.random() * 100) + 1);
  }
  return arr;
}

// Renderiza o vetor como barras
function renderArray(arr) {
  visualizationContainer.innerHTML = '';
  const maxHeight = Math.max(...arr);
  const containerHeight = visualizationContainer.clientHeight;
  const scale = containerHeight / maxHeight;
  
  arr.forEach(num => {
    const bar = document.createElement('div');
    bar.classList.add('bar');
    bar.style.height = `${num * scale * 0.9}px`; // Escala para caber no container
    visualizationContainer.appendChild(bar);
  });
}

// Função para iniciar a ordenação
startButton.addEventListener('click', async () => {
  if (isSorting) return;
  
  isSorting = true;
  startButton.disabled = true;  // Desabilita o botão de iniciar
  resetButton.disabled = true;  // Desabilita o botão de reiniciar durante a ordenação
  arraySizeInput.disabled = true; // Desabilita o ajuste de tamanho durante a ordenação
  
  const algorithm = algorithmSelect.value;
  statusText.textContent = `Ordenando com ${capitalizeFirstLetter(algorithm)}...`;

  // Cria uma cópia do array para não modificar o original
  const arrCopy = [...array];
  
  try {
    switch (algorithm) {
      case 'bubble':
        await bubbleSort(arrCopy);
        break;
      case 'selection':
        await selectionSort(arrCopy);
        break;
      case 'insertion':
        await insertionSort(arrCopy);
        break;
      case 'quick':
        await quickSort(arrCopy, 0, arrCopy.length - 1);
        break;
      default:
        return;
    }
    
    statusText.textContent = 'Ordenação Completa!';
  } catch (error) {
    console.error("Erro na ordenação:", error);
    statusText.textContent = 'Erro na ordenação!';
  } finally {
    isSorting = false;
    resetButton.disabled = false;
    arraySizeInput.disabled = false;
  }
});

// Função para capitalizar a primeira letra
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

// Função de pausa
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Bubble Sort
async function bubbleSort(arr) {
  let n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    for (let j = 0; j < n - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        // Troca os elementos
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        renderArray(arr);
        await sleep(delay);
      }
    }
  }
  return arr;
}

// Selection Sort
async function selectionSort(arr) {
  let n = arr.length;
  for (let i = 0; i < n - 1; i++) {
    let minIndex = i;
    for (let j = i + 1; j < n; j++) {
      if (arr[j] < arr[minIndex]) {
        minIndex = j;
      }
    }
    if (minIndex !== i) {
      [arr[i], arr[minIndex]] = [arr[minIndex], arr[i]];
      renderArray(arr);
      await sleep(delay);
    }
  }
  return arr;
}

// Insertion Sort
async function insertionSort(arr) {
  let n = arr.length;
  for (let i = 1; i < n; i++) {
    let key = arr[i];
    let j = i - 1;
    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
      renderArray(arr);
      await sleep(delay);
    }
    arr[j + 1] = key;
    renderArray(arr);
    await sleep(delay);
  }
  return arr;
}

// Quick Sort
async function quickSort(arr, left, right) {
  if (left < right) {
    const pivotIndex = await partition(arr, left, right);
    await quickSort(arr, left, pivotIndex - 1);
    await quickSort(arr, pivotIndex + 1, right);
  }
  
  if (left === 0 && right === arr.length - 1) {
    renderArray(arr);
    return arr;
  }
}

async function partition(arr, left, right) {
  const pivot = arr[right];
  let i = left - 1;
  
  for (let j = left; j < right; j++) {
    if (arr[j] < pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
      renderArray(arr);
      await sleep(delay);
    }
  }
  
  [arr[i + 1], arr[right]] = [arr[right], arr[i + 1]];
  renderArray(arr);
  await sleep(delay);
  
  return i + 1;
}

// Controles de música
playMusicButton.addEventListener('click', () => {
  if (backgroundMusic.src) {
    backgroundMusic.play();
    statusText.textContent = 'Música iniciada';
  } else {
    statusText.textContent = 'Por favor, selecione uma música primeiro';
  }
});

pauseMusicButton.addEventListener('click', () => {
  backgroundMusic.pause();
  statusText.textContent = 'Música pausada';
});

volumeControl.addEventListener('input', () => {
  backgroundMusic.volume = volumeControl.value;
});

musicSelect.addEventListener('change', () => {
  const selectedMusic = musicSelect.value;
  if (selectedMusic) {
    backgroundMusic.src = selectedMusic;
    backgroundMusic.load();
    statusText.textContent = 'Música carregada';
    // Reproduz a música automaticamente quando selecionada
    backgroundMusic.play();
  }
});

// Controles do YouTube
youtubeToggle.addEventListener('change', function() {
  if (this.checked) {
    youtubeControls.style.display = 'block';
    normalAudioPlayer.style.display = 'none';
    backgroundMusic.pause(); // Pausa o player de áudio normal
  } else {
    youtubeControls.style.display = 'none';
    normalAudioPlayer.style.display = 'block';
    if (youtubePlayer && typeof youtubePlayer.pauseVideo === 'function') {
      youtubePlayer.pauseVideo(); // Pausa o vídeo do YouTube se estiver reproduzindo
    }
  }
});

loadYoutubeButton.addEventListener('click', function() {
  const videoId = youtubeUrl.value.trim();
  
  if (!videoId) {
    statusText.textContent = 'Por favor, insira um ID de vídeo válido do YouTube';
    return;
  }
  
  // Limpa o container existente
  youtubePlayerContainer.innerHTML = '';
  
  // Cria o iframe para o YouTube
  const iframe = document.createElement('iframe');
  iframe.src = `https://www.youtube.com/embed/${videoId}?enablejsapi=1&autoplay=1&controls=1`;
  iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
  iframe.allowFullscreen = true;
  youtubePlayerContainer.appendChild(iframe);
  
  statusText.textContent = 'Vídeo do YouTube carregado';
});

// Inicializa a visualização com o vetor padrão
resetArray();