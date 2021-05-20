import React from 'react';
import {useDispatch, useSelector} from 'react-redux';

import {selectUserAccountAddress, selectUserAccountNet} from '../redux/reducers/user';
import {setAccountAddress, setAccountNet} from '../redux/actions';
import {Link, useLocation} from 'react-router-dom';

import {LEDGER_NAME} from '../services/constants';

import {connectToAlgoSigner} from '../utils/connectToAlgoSigner';
import './NavigationBar.scss';

const NavigationBar: React.FC = () => {
  const {pathname} = useLocation();
  const accountAddr = useSelector(selectUserAccountAddress);
  const accountNet = useSelector(selectUserAccountNet);
  const dispatch = useDispatch();

  const connectToAlgoSignerWallet = async () => {
    const fetchedAddress = await connectToAlgoSigner();

    dispatch(setAccountAddress(fetchedAddress));
    dispatch(setAccountNet(LEDGER_NAME));
  };

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <Link to="/">
          <img className="App-logo-nav" src="/logo.png" alt="AlgoSwap" />
        </Link>
        <div className={pathname === '/swap' ? 'navbar-container-active' : 'navbar-container'}>
          <Link to="/swap">
            <p>Swap</p>
          </Link>
        </div>
        <div
          className={
            pathname === '/pool' || pathname === '/create' || pathname === '/add'
              ? 'navbar-container-active'
              : 'navbar-container'
          }
        >
          <Link to="/pool">
            <p>Pool</p>
          </Link>
        </div>
      </div>
      <div className="navbar-right">
        {accountAddr ? (
          <div className="navbar-user-context">
            <div className="navbar-account-net">{accountNet}</div>
            <div className="navbar-account-addr">
              <img className="AlgoSigner-logo-nav" src="/algosigner.png" alt="AlgoSigner" />
              {accountAddr.slice(0, 10)}...{accountAddr.slice(-5)}
            </div>
          </div>
        ) : (
          <button className="navbar-connect-button" onClick={connectToAlgoSignerWallet}>
            Connect to a wallet
          </button>
        )}
      </div>
    </nav>
  );
};

export default NavigationBar;
