import React, { useRef, useEffect } from 'react';

const ELDLogPage = ({ logSheet }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      const width = 800;
      const height = 300;

      // Clear canvas with white background
      ctx.fillStyle = 'white';
      ctx.fillRect(0, 0, width, height);

      // Draw header text at top
      ctx.font = 'bold 16px Arial';
      ctx.fillStyle = '#1e293b'; // Dark color for text
      ctx.fillText('ELD Daily Log Sheet', 10, 30);
      ctx.textAlign = 'right';
      ctx.fillText(`Date: ${logSheet.date}`, width - 10, 30);
      ctx.textAlign = 'left';
      ctx.font = '14px Arial';
      ctx.fillText(`Day ${logSheet.day_number}`, 10, 50);

      // Draw the 4-row grid
      const rows = ['off_duty', 'sleeper', 'driving', 'on_duty'];
      const rowLabels = ['Off Duty', 'Sleeper', 'Driving', 'On Duty'];
      const rowHeight = 40;
      const gridStartY = 80;
      const gridWidth = 620;
      const hourSpacing = gridWidth / 24;

      // Draw vertical lines for each hour
      ctx.strokeStyle = '#ccc';
      for (let i = 0; i <= 24; i++) {
        ctx.beginPath();
        ctx.moveTo(120 + i * hourSpacing, gridStartY);
        ctx.lineTo(120 + i * hourSpacing, gridStartY + rowHeight * 4);
        ctx.stroke();

        // Draw hour numbers above the grid
        if (i % 2 === 0) {
          ctx.fillText(i.toString(), 120 + i * hourSpacing - 5, gridStartY - 5);
        }
      }

      // Draw horizontal lines separating the 4 rows
      for (let i = 0; i < 4; i++) {
        ctx.beginPath();
        ctx.moveTo(120, gridStartY + i * rowHeight);
        ctx.lineTo(120 + gridWidth, gridStartY + i * rowHeight);
        ctx.stroke();
      }

      // Draw bottom border line of the grid
      ctx.beginPath();
      ctx.moveTo(120, gridStartY + 4 * rowHeight);
      ctx.lineTo(740, gridStartY + 4 * rowHeight);
      ctx.stroke();

      // Define colors for each activity
      const colors = {
        off_duty: '#e5e7eb',
        sleeper: '#bfdbfe',
        driving: '#86efac',
        on_duty: '#f59e0b'
      };

      // Draw activity periods
      rows.forEach((row, i) => {
        logSheet.log_data[row].forEach(period => {
          const x = 120 + (period.start_hour / 24) * gridWidth;
          const width = ((period.end_hour - period.start_hour) / 24) * gridWidth;
          ctx.fillStyle = colors[row];
          ctx.fillRect(x, gridStartY + i * rowHeight, width, rowHeight);
          ctx.strokeStyle = 'black';
          ctx.strokeRect(x, gridStartY + i * rowHeight, width, rowHeight);
        });

        // Draw row labels on left side
        ctx.fillText(rowLabels[i], 10, gridStartY + i * rowHeight + 20);
      });

      // Draw totals at bottom
      ctx.font = '14px Arial';
      ctx.fillStyle = '#1e293b'; // Dark color for text
      ctx.fillText(`Off Duty: ${logSheet.log_data.total_off_duty}h | Sleeper: ${logSheet.log_data.total_sleeper}h | Driving: ${logSheet.log_data.total_driving}h | On Duty: ${logSheet.log_data.total_on_duty}h | Total: 24h`, 10, height - 10);
    }
  }, [logSheet]);

  return (
    <canvas ref={canvasRef} width={800} height={300}></canvas>
  );
};

export default ELDLogPage;
