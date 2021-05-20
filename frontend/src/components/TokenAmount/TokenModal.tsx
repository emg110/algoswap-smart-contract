/*
  Need to disable typescript check to outsmart Rodal package issue.
  If you are making any changes to the code, remove this line temporarily
  as we want to pass typecheck testing as much as possible.
*/
// @ts-nocheck
import React from 'react';

/* eslint-disable */
import Rodal from 'rodal';

import 'rodal/lib/rodal.css';
import './TokenModal.scss';

interface Props {
  selectedToken: string;
  tokenList?: Array<Array<string>>;

  updateSelectedToken: (token: string) => void;
  openTokenModal: boolean;
  toggleTokenModal: () => void;
}

const TokenModal: React.FC<Props> = ({
  selectedToken,
  tokenList,
  updateSelectedToken,
  openTokenModal,
  toggleTokenModal,
}) => {
  const modalStyle = {
    position: 'relative',
    borderRadius: '30px',
    top: '210px',
  };

  return (
    <Rodal
      width={420}
      customStyles={modalStyle}
      visible={openTokenModal}
      onClose={toggleTokenModal}
      height={500}
      showCloseButton={false}
    >
      <div className="token-modal">
        <div className="token-modal-header">
          <div className="token-modal-header-image">
            <img className="App-logo-modal" src="/logo.png" alt="AlgoSwap" />
          </div>
          Select a token
        </div>
        <div className="token-modal-list">
          {tokenList &&
            tokenList.map(token => {
              if (token[0] === selectedToken) {
                return (
                  <div
                    className={['token-modal-list-token', 'token-modal-list-active'].join(' ')}
                    key={token[1]}
                    onClick={() => updateSelectedToken(token[0])}
                  >
                    {token[0]}
                  </div>
                );
              }
              return (
                <div
                  className="token-modal-list-token"
                  key={token[1]}
                  onClick={() => updateSelectedToken(token[0])}
                >
                  {token[0]}
                </div>
              );
            })}
        </div>
        <div className="token-modal-footer">
          <button className="token-modal-footer-button" onClick={toggleTokenModal}>
            Close
          </button>
        </div>
      </div>
    </Rodal>
  );
};

export default TokenModal;
