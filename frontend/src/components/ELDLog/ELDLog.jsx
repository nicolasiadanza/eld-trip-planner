import React from 'react';
import ELDLogPage from './ELDLogPage';

const ELDLog = ({ tripData }) => {
  if (!tripData || !tripData.log_sheets) {
    return null;
  }

  return (
    <div>
      <h1>ELD Log Sheets</h1>
      {tripData.log_sheets.map((logSheet, index) => (
        <div key={index} className="log-card">
          <ELDLogPage logSheet={logSheet} />
        </div>
      ))}
    </div>
  );
};

export default ELDLog;
