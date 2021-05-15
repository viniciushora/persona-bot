import React, { Component } from "react";
import {
  Card,
  Icon,
  IconButton,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody
} from "@material-ui/core";

const TableCard = props => {

  return (
    <Card elevation={3} className="pt-20 mb-24">
      <div className="card-title px-24 mb-12">Personagens</div>
      <div className="overflow-auto">
        <Table className="product-table">
          <TableHead>
            <TableRow>
              <TableCell className="px-24" colSpan={4}>
                Nome
              </TableCell>
              <TableCell className="px-0" colSpan={2}>
                ID
              </TableCell>
              <TableCell className="px-0" colSpan={2}>
                Jogador
              </TableCell>
              <TableCell className="px-0" colSpan={1}>
                Ação
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.personagens.map((personagem, index) => (
              <TableRow key={index}>
                <TableCell className="px-0 capitalize" colSpan={4} align="left">
                  <div className="flex flex-middle">
                  <img
                      className="circular-image-small"
                      src={personagem.foto}
                      alt="user"
                    />
                    <p className="m-0 ml-8">{personagem.nome}</p>
                  </div>
                </TableCell>
                <TableCell className="px-0 capitalize" align="left" colSpan={2}>
                  <p className="m-0 ml-8">{personagem.personagem_id}</p>
                </TableCell>
                <TableCell className="px-0 capitalize" align="left" colSpan={2}>
                  <p className="m-0 ml-8">{personagem.usuario}</p>
                </TableCell>
                <TableCell className="px-0" colSpan={1}>
                  <IconButton>
                    <Icon color="primary">edit</Icon>
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </Card>
  );
};

export default TableCard;