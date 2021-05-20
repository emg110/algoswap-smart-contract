import React from 'react';
import {Link} from 'react-router-dom';

import './LiquidityList.scss';

export default class LiquidityList extends React.PureComponent<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      liquidities: [],
    };
  }

  renderLiquidities = () => {
    return this.state.liquidities.map(liquidity => (
      <div className="liquidity-list-liquidity">{liquidity}</div>
    ));
  };

  render() {
    return (
      <div className="liquidity-list">
        <div className="liquidity-list-header">
          <p className="liquidity-list-header-title">Your liquidity</p>
          <div className="liquidity-list-header-buttons">
            <Link to="/create">
              <button type="button" className="liquidity-list-header-buttons-create-pair">
                Create a pair
              </button>
            </Link>
            <Link to="/add">
              <button type="button" className="liquidity-list-header-buttons-add-liquidity">
                Add liquidity
              </button>
            </Link>
          </div>
        </div>
        <div className="liquidity-list-content">
          {this.state.liquidities.length > 0 ? (
            this.renderLiquidities()
          ) : (
            <p className="liquidity-list-content-nullstate">No liquidity found.</p>
          )}
        </div>
      </div>
    );
  }
}

interface Props {}
interface State {
  liquidities: string[];
}
