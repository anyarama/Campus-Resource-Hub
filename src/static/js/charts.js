/**
 * Chart.js Helper Functions
 * IU-Branded Chart Configurations
 * 
 * AI Contribution: Initial Chart.js wrapper structure and IU color palette
 * Reviewed and customized by developer on 2025-11-09
 */

import { Chart, registerables } from 'chart.js/auto';

// Register all Chart.js components
Chart.register(...registerables);

// IU Brand Colors
const IU_COLORS = {
  crimson: '#DC143C',
  darkCrimson: '#B30000',
  lightCrimson: '#FF6B88',
  cream: '#F5F1E8',
  darkCream: '#E5DFC8',
  charcoal: '#2C2C2C',
  slate: '#6B6B6B',
  lightGray: '#E8E8E8',
  success: '#28A745',
  warning: '#FFC107',
  info: '#17A2B8',
};

// Chart.js default overrides for IU theme
const IU_CHART_DEFAULTS = {
  font: {
    family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
    size: 13,
    weight: '400',
  },
  color: IU_COLORS.charcoal,
  responsive: true,
  maintainAspectRatio: true,
};

/**
 * Apply theme-aware colors based on current theme
 * @returns {Object} Theme-specific colors
 */
function getThemeColors() {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  
  return {
    textColor: isDark ? '#E8E8E8' : IU_COLORS.charcoal,
    gridColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
    borderColor: isDark ? 'rgba(255, 255, 255, 0.2)' : 'rgba(0, 0, 0, 0.1)',
    backgroundColor: isDark ? '#1a1a1a' : '#ffffff',
  };
}

/**
 * Create a Line Chart with IU styling
 * 
 * @param {HTMLCanvasElement} canvas - Canvas element to render chart
 * @param {Object} config - Chart configuration
 * @param {string[]} config.labels - X-axis labels (e.g., dates)
 * @param {Object[]} config.datasets - Array of dataset objects
 * @param {string} config.datasets[].label - Dataset label
 * @param {number[]} config.datasets[].data - Data points
 * @param {string} [config.datasets[].color] - Optional color override
 * @param {Object} [config.options] - Additional Chart.js options
 * @returns {Chart} Chart.js instance
 * 
 * @example
 * createLineChart(canvas, {
 *   labels: ['Jan', 'Feb', 'Mar'],
 *   datasets: [{
 *     label: 'Bookings',
 *     data: [12, 19, 15]
 *   }]
 * });
 */
export function createLineChart(canvas, config) {
  const themeColors = getThemeColors();
  
  // Process datasets with IU branding
  const datasets = config.datasets.map((dataset, index) => {
    const color = dataset.color || (index === 0 ? IU_COLORS.crimson : IU_COLORS.slate);
    
    return {
      label: dataset.label,
      data: dataset.data,
      borderColor: color,
      backgroundColor: `${color}20`, // 20% opacity
      borderWidth: 2,
      fill: dataset.fill !== false, // Fill by default
      tension: 0.4, // Smooth curves
      pointRadius: 4,
      pointHoverRadius: 6,
      pointBackgroundColor: color,
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointHoverBackgroundColor: color,
      pointHoverBorderColor: '#fff',
    };
  });

  const chartConfig = {
    type: 'line',
    data: {
      labels: config.labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 2.5,
      plugins: {
        legend: {
          display: true,
          position: 'top',
          align: 'start',
          labels: {
            font: IU_CHART_DEFAULTS.font,
            color: themeColors.textColor,
            padding: 16,
            usePointStyle: true,
            pointStyle: 'circle',
          },
        },
        tooltip: {
          backgroundColor: themeColors.backgroundColor,
          titleColor: themeColors.textColor,
          bodyColor: themeColors.textColor,
          borderColor: themeColors.borderColor,
          borderWidth: 1,
          padding: 12,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function(context) {
              let label = context.dataset.label || '';
              if (label) {
                label += ': ';
              }
              if (context.parsed.y !== null) {
                label += context.parsed.y;
              }
              return label;
            }
          }
        },
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            font: IU_CHART_DEFAULTS.font,
            color: themeColors.textColor,
          },
          border: {
            color: themeColors.borderColor,
          },
        },
        y: {
          beginAtZero: true,
          grid: {
            color: themeColors.gridColor,
            drawBorder: false,
          },
          ticks: {
            font: IU_CHART_DEFAULTS.font,
            color: themeColors.textColor,
            padding: 8,
          },
          border: {
            display: false,
          },
        },
      },
      interaction: {
        mode: 'index',
        intersect: false,
      },
      ...config.options,
    },
  };

  return new Chart(canvas, chartConfig);
}

export function createBarChart(canvas, config) {
  const themeColors = getThemeColors();

  const datasets = config.datasets.map((dataset, index) => {
    const color = dataset.color || IU_COLORS.crimson;
    return {
      label: dataset.label,
      data: dataset.data,
      backgroundColor: dataset.backgroundColor || color,
      borderRadius: dataset.borderRadius || 8,
      maxBarThickness: dataset.maxBarThickness || 48,
    };
  });

  const chartConfig = {
    type: 'bar',
    data: {
      labels: config.labels,
      datasets,
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: config.options?.legend !== false,
          position: 'top',
          labels: {
            font: IU_CHART_DEFAULTS.font,
            color: themeColors.textColor,
          },
        },
        tooltip: {
          backgroundColor: themeColors.backgroundColor,
          titleColor: themeColors.textColor,
          bodyColor: themeColors.textColor,
          borderColor: themeColors.borderColor,
          borderWidth: 1,
        },
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            color: themeColors.textColor,
            font: IU_CHART_DEFAULTS.font,
          },
        },
        y: {
          beginAtZero: true,
          grid: { color: themeColors.gridColor },
          ticks: {
            color: themeColors.textColor,
            font: IU_CHART_DEFAULTS.font,
          },
        },
      },
      ...config.options,
    },
  };

  return new Chart(canvas, chartConfig);
}

/**
 * Create a Doughnut Chart with IU styling
 * 
 * @param {HTMLCanvasElement} canvas - Canvas element to render chart
 * @param {Object} config - Chart configuration
 * @param {string[]} config.labels - Segment labels
 * @param {number[]} config.data - Data values
 * @param {string[]} [config.colors] - Optional color array (uses IU palette by default)
 * @param {Object} [config.options] - Additional Chart.js options
 * @returns {Chart} Chart.js instance
 * 
 * @example
 * createDoughnutChart(canvas, {
 *   labels: ['Study Rooms', 'Equipment', 'Spaces'],
 *   data: [45, 30, 25]
 * });
 */
export function createDoughnutChart(canvas, config) {
  const themeColors = getThemeColors();
  
  // Default IU color palette for segments
  const defaultColors = [
    IU_COLORS.crimson,
    IU_COLORS.darkCrimson,
    IU_COLORS.lightCrimson,
    IU_COLORS.slate,
    IU_COLORS.info,
    IU_COLORS.warning,
    IU_COLORS.success,
  ];
  
  const colors = config.colors || defaultColors;
  const backgroundColors = colors.slice(0, config.data.length);
  const hoverColors = backgroundColors.map(color => {
    // Lighten color on hover
    return color + 'DD'; // Add slight opacity
  });

  const chartConfig = {
    type: 'doughnut',
    data: {
      labels: config.labels,
      datasets: [{
        data: config.data,
        backgroundColor: backgroundColors,
        hoverBackgroundColor: hoverColors,
        borderWidth: 2,
        borderColor: themeColors.backgroundColor,
        hoverBorderColor: themeColors.backgroundColor,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 1.5,
      cutout: '65%', // Size of center hole
      plugins: {
        legend: {
          display: true,
          position: 'right',
          align: 'center',
          labels: {
            font: IU_CHART_DEFAULTS.font,
            color: themeColors.textColor,
            padding: 16,
            usePointStyle: true,
            pointStyle: 'circle',
            generateLabels: function(chart) {
              const data = chart.data;
              if (data.labels.length && data.datasets.length) {
                return data.labels.map((label, i) => {
                  const value = data.datasets[0].data[i];
                  const total = data.datasets[0].data.reduce((a, b) => a + b, 0);
                  const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                  
                  return {
                    text: `${label} (${percentage}%)`,
                    fillStyle: data.datasets[0].backgroundColor[i],
                    hidden: false,
                    index: i,
                  };
                });
              }
              return [];
            }
          },
        },
        tooltip: {
          backgroundColor: themeColors.backgroundColor,
          titleColor: themeColors.textColor,
          bodyColor: themeColors.textColor,
          borderColor: themeColors.borderColor,
          borderWidth: 1,
          padding: 12,
          cornerRadius: 8,
          displayColors: true,
          callbacks: {
            label: function(context) {
              const label = context.label || '';
              const value = context.parsed;
              const total = context.dataset.data.reduce((a, b) => a + b, 0);
              const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
              return `${label}: ${value} (${percentage}%)`;
            }
          }
        },
      },
      interaction: {
        mode: 'point',
      },
      ...config.options,
    },
  };

  return new Chart(canvas, chartConfig);
}

/**
 * Destroy chart instance and clean up
 * @param {Chart} chart - Chart.js instance to destroy
 */
export function destroyChart(chart) {
  if (chart && typeof chart.destroy === 'function') {
    chart.destroy();
  }
}

/**
 * Update chart data dynamically
 * @param {Chart} chart - Chart.js instance
 * @param {Object} newData - New data object with labels and datasets
 */
export function updateChartData(chart, newData) {
  if (!chart) return;
  
  if (newData.labels) {
    chart.data.labels = newData.labels;
  }
  
  if (newData.datasets) {
    chart.data.datasets = newData.datasets;
  }
  
  chart.update('active'); // Animate update
}

/**
 * Export chart as base64 image
 * @param {Chart} chart - Chart.js instance
 * @returns {string} Base64 encoded image
 */
export function exportChartImage(chart) {
  if (!chart) return null;
  return chart.toBase64Image();
}

// Listen for theme changes and update charts
if (typeof window !== 'undefined') {
  window.addEventListener('theme-changed', () => {
    // Trigger chart updates on theme change
    const event = new CustomEvent('charts-theme-changed');
    window.dispatchEvent(event);
  });
}

export { IU_COLORS };
