import React from 'react';
import { Pagination as BootstrapPagination } from 'react-bootstrap';

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
    const handlePageChange = (page) => {
        if (page >= 1 && page <= totalPages) {
            onPageChange(page);
        }
    };

    const getPageItems = () => {
        const items = [];
        const maxVisiblePages = 5;
        const startPage = Math.max(currentPage - Math.floor(maxVisiblePages / 2), 1);
        const endPage = Math.min(startPage + maxVisiblePages - 1, totalPages);

        for (let page = startPage; page <= endPage; page++) {
            items.push(
                <BootstrapPagination.Item
                    key={page}
                    active={page === currentPage}
                    onClick={() => handlePageChange(page)}
                >
                    {page}
                </BootstrapPagination.Item>
            );
        }

        return items;
    };

    return (
        <BootstrapPagination>
            <BootstrapPagination.First onClick={() => handlePageChange(1)} disabled={currentPage === 1} />
            <BootstrapPagination.Prev onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1} />
            {getPageItems()}
            <BootstrapPagination.Next onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages} />
            <BootstrapPagination.Last onClick={() => handlePageChange(totalPages)} disabled={currentPage === totalPages} />
        </BootstrapPagination>
    );
};

export default Pagination;
