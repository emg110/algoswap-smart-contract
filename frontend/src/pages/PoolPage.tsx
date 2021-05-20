import React from 'react';

import LiquidityList from '../components/LiquidityList';
import './PoolPage.scss';

const PoolPage: React.FC = () => {
  return (
    <div className="pool-page">
      <LiquidityList />
    </div>
  );
};

export default PoolPage;
